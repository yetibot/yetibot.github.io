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
