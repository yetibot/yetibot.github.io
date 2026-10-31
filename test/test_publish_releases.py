import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SPEC = importlib.util.spec_from_file_location(
    "publisher", Path(__file__).parents[1] / "scripts/publish_releases.py")
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)

VERSION = "20261031.203010.6700557c"
PAYLOAD = {"version": VERSION, "sha": "6700557c" + "0" * 32,
           "run_number": 10, "run_attempt": 1}
MANIFEST = {
    "schema_version": 1,
    "build": {"app": {"version": VERSION, "revision": "6700557c",
                       "commit_url": "https://github.com/yetibot/yetibot/commit/6700557c"},
              "core": None},
    "changes": [{"id": "release-info", "date": "2026-10-31",
                 "component": "app", "title": "Discover features",
                 "summary": "Read bundled notes.", "commands": ["version"],
                 "requires": [], "links": []}]}


def encoded(value):
    return (json.dumps(value, indent=2) + "\n").encode()


class PublicationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_publishes_exact_archive_and_latest_bytes(self):
        publisher.publish(PAYLOAD, encoded(MANIFEST), self.root)
        self.assertEqual((self.root / f"{VERSION}.json").read_bytes(),
                         encoded(MANIFEST))
        self.assertEqual((self.root / "latest.json").read_bytes(),
                         encoded(MANIFEST))
        self.assertEqual(json.loads((self.root / "publication.json").read_text()),
                         PAYLOAD)

    def test_replay_is_idempotent_and_versions_are_immutable(self):
        publisher.publish(PAYLOAD, encoded(MANIFEST), self.root)
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        publisher.publish(PAYLOAD, encoded(MANIFEST), self.root)
        self.assertEqual(before, {p.name: p.read_bytes()
                                  for p in self.root.iterdir()})
        changed = copy.deepcopy(MANIFEST)
        changed["changes"][0]["summary"] = "Different content."
        with self.assertRaises(ValueError):
            publisher.publish(PAYLOAD, encoded(changed), self.root)
        self.assertEqual(before, {p.name: p.read_bytes()
                                  for p in self.root.iterdir()})

    def test_late_older_run_cannot_roll_back_latest(self):
        publisher.publish(PAYLOAD, encoded(MANIFEST), self.root)
        old = copy.deepcopy(MANIFEST)
        version = "20261030.120000.1234567"
        old["build"]["app"] = {"version": version, "revision": "1234567",
                                 "commit_url": "https://github.com/yetibot/yetibot/commit/1234567"}
        payload = {"version": version, "sha": "1234567" + "0" * 33,
                   "run_number": 9, "run_attempt": 1}
        publisher.publish(payload, encoded(old), self.root)
        self.assertEqual((self.root / "latest.json").read_bytes(), encoded(MANIFEST))
        self.assertTrue((self.root / f"{version}.json").exists())

    def test_rejects_invalid_payload_before_writing(self):
        for change in [{"version": "../../escape"}, {"sha": "f" * 40},
                       {"run_number": True}, {"url": "https://elsewhere.invalid"}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                publisher.publish(dict(PAYLOAD, **change), encoded(MANIFEST),
                                  self.root)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_rejects_extra_private_fields_and_wrong_schema(self):
        for change in [{"schema_version": 2}, {"credential": "not-public"}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                publisher.publish(PAYLOAD, encoded(dict(MANIFEST, **change)),
                                  self.root)
        bad = copy.deepcopy(MANIFEST)
        bad["build"]["app"]["commit_url"] = "https://elsewhere.invalid"
        with self.assertRaises(ValueError):
            publisher.publish(PAYLOAD, encoded(bad), self.root)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_json_body_limit(self):
        with self.assertRaises(ValueError):
            publisher.publish(PAYLOAD, b"x" * (publisher.MAX_MANIFEST + 1),
                              self.root)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_extracts_only_the_known_bundled_json_not_zip_paths(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as jar:
            jar.writestr("../../escape", "do not extract")
            jar.writestr("yetibot/release-info.json", encoded(MANIFEST))
        with patch.object(publisher, "download_jar", return_value=data.getvalue()):
            self.assertEqual(publisher.download_manifest(VERSION), encoded(MANIFEST))
        self.assertFalse((self.root.parent / "escape").exists())

    def test_restores_published_json_without_copying_or_executing_site_code(self):
        repo = self.root / "repo"
        repo.mkdir()
        def git(*args):
            return subprocess.run(["git", "-C", str(repo), *args], check=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git("init", "-q")
        data = repo / "releases"
        publisher.publish(PAYLOAD, encoded(MANIFEST), data)
        (repo / "evil.sh").write_text("exit 99\n")
        git("add", "releases", "evil.sh")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-qm", "Published data")
        target = self.root / "restored"
        publisher.restore("HEAD", target, repo)
        self.assertEqual(sorted(p.name for p in target.iterdir()),
                         [f"{VERSION}.json", "latest.json", "publication.json"])
        self.assertEqual((target / "latest.json").read_bytes(), encoded(MANIFEST))


if __name__ == "__main__":
    unittest.main()
