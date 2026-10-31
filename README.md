# yetibot.github.io

[![Build Status](https://github.com/yetibot/yetibot.github.io/actions/workflows/deploy.yml/badge.svg?branch=source)](https://github.com/yetibot/yetibot.github.io/actions/workflows/deploy.yml)

This is the static site generator source for
[https://yetibot.com](https://yetibot.com).

It's built on [Cryogen](http://cryogenweb.org/).

## Prerequisites

- [Leiningen](https://github.com/technomancy/leiningen)
- [Sass](https://sass-lang.com/install)

  e.g.

  ```
  npm install -g sass
  ```
- [yarn or npm](https://yarnpkg.com/en/)


## Dev usage

Run a Ring server for local dev:

```bash
PORT=4040 lein ring server
```

### JavaScript

```bash
yarn install
```

Edit `src/index.js` and run:

```bash
yarn dev:watch
```

This will compile the JS with Webpack. Currently does not transpile.

A git pre-commit hook will compile the JS for production.

## Build

Generate the static site:

```bash
lein run
```

## Release JSON

The application release workflow sends a `yetibot-release-info` repository
dispatch with only its version, full SHA, workflow run number and attempt.
The publisher downloads the already-published public Clojars app JAR and reads
only its bounded `yetibot/release-info.json` member. It never executes JAR code,
follows download redirects, extracts arbitrary ZIP paths or receives provider
credentials. The schema and publication identity are validated before writing.

`/releases/latest.json` contains the complete public manifest;
`/releases/<version>.json` archives are immutable. `publication.json` orders
updates by the app release workflow's run number and attempt, so a late older
job cannot roll back latest. Replays are idempotent; conflicting archives fail.
These are published builds, not proof that an individual bot has deployed them.

The protected `source` branch is never written by the publisher. Every build
restores only validated JSON from the existing Pages `master` branch before
Cryogen cleans/rebuilds the output, then the existing Pages action publishes
assets and data together. Production jobs are serialized. A failed validation
or download stops deployment instead of deleting existing release data. First
publication waits for an app release containing the bundled manifest.

Test the publisher without network access:

```sh
python3 -m unittest discover -s test -v
```
