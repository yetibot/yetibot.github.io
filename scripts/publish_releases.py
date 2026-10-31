"""Publish public release data without writing the protected source branch."""
import argparse
from datetime import date
import io
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import urllib.request
import zipfile

MAX_MANIFEST = 512 * 1024
MAX_JAR = 32 * 1024 * 1024
VERSION = re.compile(r"[0-9]{8}\.[0-9]{6}\.([0-9a-f]{7,40})")
ARCHIVE = re.compile(r"releases/[0-9]{8}\.[0-9]{6}\.[0-9a-f]{7,40}\.json")
DESTINATION = Path("resources/templates/releases")


def require(condition):
    if not condition:
        raise ValueError("Invalid public release data.")


def text(value, maximum):
    return (isinstance(value, str) and bool(value.strip())
            and 1 <= len(value.encode("utf-16-le")) // 2 <= maximum
            and not any(unicodedata.category(c) == "Cc" for c in value))


def texts(value, maximum):
    return isinstance(value, list) and len(value) <= 5 and all(
        text(item, maximum) for item in value)


def valid_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_manifest(data):
    require(isinstance(data, dict)
            and set(data) == {"schema_version", "build", "changes"}
            and type(data["schema_version"]) is int and data["schema_version"] == 1)
    require(isinstance(data["build"], dict) and set(data["build"]) == {"app", "core"})
    for component, entry in data["build"].items():
        if entry is None:
            continue
        require(isinstance(entry, dict)
                and set(entry) == {"version", "revision", "commit_url"})
        version = entry["version"]
        require(isinstance(version, str)
                and re.fullmatch(r"[0-9][0-9A-Za-z._+-]{0,127}", version))
        match = VERSION.fullmatch(version)
        revision = match.group(1) if match else None
        repository = "yetibot" if component == "app" else "core"
        url = f"https://github.com/yetibot/{repository}/commit/{revision}" if revision else None
        require(entry["revision"] == revision and entry["commit_url"] == url)
    changes = data["changes"]
    require(isinstance(changes, list) and len(changes) <= 200)
    ids = set()
    for item in changes:
        require(isinstance(item, dict) and set(item) == {
            "id", "date", "component", "title", "summary", "commands", "requires", "links"})
        require(isinstance(item["id"], str)
                and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", item["id"])
                and item["id"] not in ids)
        ids.add(item["id"])
        require(valid_date(item["date"]) and item["component"] in ("app", "core")
                and text(item["title"], 120) and text(item["summary"], 800)
                and texts(item["commands"], 240) and texts(item["requires"], 240)
                and texts(item["links"], 200))
        require(all(re.fullmatch(
            r"https://github\.com/yetibot/(?:yetibot|core)/(?:pull/[0-9]+|commit/[0-9a-f]{7,40})",
            link) for link in item["links"]))
    return data


def load_manifest(body):
    require(len(body) <= MAX_MANIFEST)
    return validate_manifest(json.loads(body.decode("utf-8")))


def validate_publication(payload):
    require(isinstance(payload, dict) and set(payload) == {
        "version", "sha", "run_number", "run_attempt"})
    require(isinstance(payload["version"], str)
            and VERSION.fullmatch(payload["version"]))
    require(isinstance(payload["sha"], str)
            and re.fullmatch(r"[0-9a-f]{40}", payload["sha"])
            and payload["sha"].startswith(VERSION.fullmatch(payload["version"]).group(1)))
    require(all(type(payload[key]) is int and payload[key] > 0
                for key in ("run_number", "run_attempt")))
    return payload


def publish(payload, body, destination=DESTINATION):
    validate_publication(payload)
    manifest = load_manifest(body)
    require(manifest["build"]["app"] is not None
            and manifest["build"]["app"]["version"] == payload["version"])
    archive = destination / f"{payload['version']}.json"
    publication = destination / "publication.json"
    latest = destination / "latest.json"
    previous = None
    if publication.exists():
        previous = validate_publication(json.loads(publication.read_text()))
        require(latest.exists()
                and load_manifest(latest.read_bytes())["build"]["app"]["version"]
                == previous["version"])
    require(not archive.exists() or load_manifest(archive.read_bytes()) == manifest)
    def order(value):
        return value["run_number"], value["run_attempt"]
    if previous and order(payload) == order(previous):
        require(payload == previous)
    destination.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        archive.write_bytes(body)
    if previous is None or order(payload) >= order(previous):
        latest.write_bytes(archive.read_bytes())
        publication.write_text(json.dumps(payload, indent=2) + "\n")
    return {"archived": True, "updated_latest": previous is None
            or order(payload) >= order(previous)}


def restore(ref, destination=DESTINATION, repo=Path(".")):
    """Only restore validated data blobs, never execute/extract the Pages tree."""
    def git(*args):
        return subprocess.run(["git", "-C", str(repo), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    paths = git("ls-tree", "-rz", "--name-only", ref, "--", "releases").split(b"\0")
    files = {}
    for raw in filter(None, paths):
        path = raw.decode("utf-8")
        if not (ARCHIVE.fullmatch(path)
                or path in ("releases/latest.json", "releases/publication.json")):
            continue
        require(int(git("cat-file", "-s", f"{ref}:{path}")) <= MAX_MANIFEST)
        body = git("show", f"{ref}:{path}")
        if path.endswith("/publication.json"):
            validate_publication(json.loads(body))
        else:
            manifest = load_manifest(body)
            if ARCHIVE.fullmatch(path):
                require(path == f"releases/{manifest['build']['app']['version']}.json")
        files[Path(path).name] = body
    destination.mkdir(parents=True, exist_ok=True)
    for name, body in files.items():
        (destination / name).write_bytes(body)
    return len(files)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def download_jar(version):
    require(isinstance(version, str) and VERSION.fullmatch(version))
    url = f"https://repo.clojars.org/yetibot/yetibot/{version}/yetibot-{version}.jar"
    request = urllib.request.Request(url, headers={"User-Agent": "yetibot-release-publisher"})
    with urllib.request.build_opener(NoRedirect).open(request, timeout=15) as response:
        require(response.status == 200)
        body = response.read(MAX_JAR + 1)
        require(len(body) <= MAX_JAR)
        return body


def download_manifest(version):
    with zipfile.ZipFile(io.BytesIO(download_jar(version))) as jar:
        name = "yetibot/release-info.json"
        require(jar.getinfo(name).file_size <= MAX_MANIFEST)
        with jar.open(name) as stream:
            body = stream.read(MAX_MANIFEST + 1)
            require(len(body) <= MAX_MANIFEST)
            return body


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("restore").add_argument("--ref", required=True)
    commands.add_parser("publish").add_argument("--event", required=True)
    args = parser.parse_args()
    if args.command == "restore":
        print(json.dumps({"restored": restore(args.ref)}))
    else:
        payload = json.loads(Path(args.event).read_text())["client_payload"]
        validate_publication(payload)
        print(json.dumps(publish(payload, download_manifest(payload["version"]))))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        raise SystemExit("Release publication failed validation or retrieval.")
