{:title "Operations Guide"
 :subtitle "Running and operating a Yetibot"
 :layout :page
 :toc true
 :page-index 2
 :navbar? true}

<!-- can't indent this properly because Markdown turns it into a code block -->
<article class="message is-info">
<div class="message-header">
  <p>Tip</p>
</div>
<div class="message-body">
  This guide is all about running and operating a Yetibot. It documents system
  dependencies, Docker usage, and configuration mechanisms.

- If you're more interested using Yetibot, check out the
  [User Guide](/user-guide).
- If you're more interested in Yetibot's internals or building features, check
  out the [Developer Guide](/dev-guide).
</div>
</article>

<article class="message is-info">
<div class="message-header">
  <p>Getting help</p>
</div>
<div class="message-body">
  Although we hope the docs are useful and comprehensive,
  **don't hesitate to ask for help in [Slack](https://slack.yetibot.com)!**
  It could potentially save you a lot of time.
</div>
</article>

## Up and running

To get a Yetibot running you need:

1. Some config
1. A Postgres database
1. A way to run it (i.e. `docker` or `lein`)

### Docker Compose

Docker Compose satisfies these requirements very quickly. Run from the root of
the [Yetibot repo](https://github.com/yetibot/yetibot):

```bash
docker-compose up
```

This starts up a Postgres container and a Yetibot container, configured to
connect to IRC as user name `yetibot_demo`. Once it's up check out
[http://localhost:3456](http://localhost:3456) to view the dashboard.

See the [docker-compose.yml](https://github.com/yetibot/yetibot/blob/master/docker-compose.yml) file to look at exactly how
these containers are configured. This demonstrates a very minimal default config
that you can modify. For example, you could use Slack instead by switching to a
config like:

```yaml
    environment:
      - YB_ADAPTERS_SLACK_TYPE=slack
      - YB_ADAPTERS_SLACK_TOKEN=xoxb-my-token
      - YB_DB_URL=postgresql://yetibot:yetibot@postgres:5432/yetibot
```

### Kubernetes with Helm

Running on Kubernetes is super simple with the official
[yetibot-helm](https://github.com/yetibot/yetibot-helm) chart.

### Minimal config

A very minimal config would be `config/config.edn`:

```clojure
{:yetibot
  {:adapters {:freenode {:type "irc",
                        :username "my-yetibot",
                        :host "chat.freenode.net",
                        :port "7070",
                        :ssl "true"}}}}
```

This instructs Yetibot to join freenode with the username `my-yetibot` (change
it to whatever you like).

If you don't configure a Postgres database, it defaults to:

```bash
postgresql://localhost:5432/yetibot
```

It expects the database to already exist, but any tables will be created
idempotently on startup. To override the default connection string along with
the above config, it'd look like:

```clojure
{:yetibot
 {:adapters {:freenode {:type "irc",
                        :username "my-yetibot",
                        :host "chat.freenode.net",
                        :port "7070",
                        :ssl "true"}}
  :db {:url "postgresql://user:pass@mydb:5432/yetibot"}}}
```

For full config see the
[CONFIGURATION](https://github.com/yetibot/yetibot.core/blob/master/doc/CONFIGURATION.md)
docs (TODO move these to the site).

### Postgres

There are many ways to install Postgres. Here we demonstrate two common
approaches:

#### Docker

As usual, Docker makes things easier when it comes to infra:

```bash

docker run -d -p 5432:5432 --name postgres \
  --restart="always" \
  -v /pgdata:/var/lib/postgresql/data \
  -e POSTGRES_USER="yetibot" \
  -e POSTGRES_PASSWORD="yetibot" \
  -e POSTGRES_DB="yetibot" \
  postgres:latest

docker logs -f postgres

# to remove postgres docker container

docker rm -f postgres
```

Assuming you use a Docker link from another container to this container, the
connection string is then:

```bash
postgresql://yetibot:yetibot@postgres:5432/yetibot
```

As an example of Docker linking, you could use `psql` from another container
like:

```bash
docker run --rm -it --link postgres postgres bash
psql -h postgres -U yetibot
\l
\q
exit
```

#### Ubuntu VM

Much of this is borrowed from
[DigitalOcean's docs](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04):

```bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo -u postgres psql
createdb yetibot
```

### Run it

There are a few ways to quickly run a Yetibot:

1. Docker - [read the Yetibot on Docker docs](https://yetibot.com/ops-guide/#docker)
1. Grab an archive of the source from the [Yetibot
   releases](https://github.com/yetibot/yetibot/releases), unzip, put the config
   in place and `lein run`
1. Clone the source of this repo, put the config in place and `lein run`

As an example, here's how you could get the latest code from `master`, extract,
put config in place, and run it (assumes you already have
[Leiningen](https://github.com/technomancy/leiningen) installed):

```bash
cd /tmp
curl https://codeload.github.com/yetibot/yetibot/tar.gz/master | tar xvz
cd yetibot-master
cat << EOF > config.edn
{:yetibot
 {:adapters
  {:freenode
   {:type "irc"
    :username "my-yetibot"
    :host "chat.freenode.net"
    :port "7070"
    :ssl "true"}}}}
EOF
YB_LOG_LEVEL=debug CONFIG_PATH=config.edn lein run
```

Once it starts up you'll see a log like:

```bash
17-05-28 23:27:56 deep.local INFO [yetibot.core.loader:41] - ☑ Loaded 84 namespaces matching [#"^yetibot\.(core\.)?commands.*" #"^.*plugins\.commands.*"]
```

At this point it should be connected to Freenode. Trying running a command
against it:

```bash
/msg my-yetibot !echo Hello, Yetibot!
```

And you should get a reply:

```bash
my-yetibot: Hello, Yetibot!
```

## Configuration

Yetibot can be fully configured via one or more mechanisms, in order of
precedence with the first overriding the next:

- environment variables
- `leiningen` profiles EDN file
- a config EDN file

When multiple methods are specified the values are merged.

See sample configuration files in both formats:

- [profiles.sample.clj](https://github.com/yetibot/yetibot.core/blob/master/config/profiles.sample.clj)
- [config.sample.edn](https://github.com/yetibot/yetibot.core/blob/master/config/config.sample.edn)

These are equivalent and both immutable (meaning they cannot change at runtime).

### Rationale

Yetibot supports both immutable and mutable configuration, for configuring
different parts of the system.

It's useful to change the configuration of a system at runtime in certain
situations. It would be burdensome to have to login to a system where Yetibot
runs, change config and restart Yetibot.

On the other hand, the benefits of immutability are well-known. Explicitly
separating out the small amount of mutable config from the majority of immutable
config lets us maximize immutability benefits and minimize negative affects of
mutability in our system.

<article class="message is-info">
<div class="message-header">
  <p>Note</p>
</div>
<div class="message-body">
  In the future we may move all mutable configuration to the database.
</div>
</article>

### Modes

#### Immutable

**Immutable config sources** include both `profiles.clj` and environmental
variables via `environ` and loading EDN from a file at `config/config.edn`
(this can be overridden by specifying a `CONFIG_PATH` env var).

Any config specified in an EDN file will be overridden by values provided by
`environ`. Environment config can be explicitly ignored by setting an
environment variable `YETIBOT_ENV_CONFIG_DISABLED=true`.

Providing config via multiple methods
makes it compatible with 12-factor configuration and simple usage in container
environments while still retaining the ease of use of the EDN file option.

The majority of configurable sub-systems use immutable config as they do not
need to change very often. Examples include:

- Chat adapters
- Twitter credentials
- Postgres connection string
- etc.

#### Mutable

**Mutable config source** is an EDN file stored at `./config/mutable.edn` by
default. `CONFIG_MUTABLE` can optionally be defined to specify a custom
location. Yetibot reads and writes to this file at runtime, so it should not
be modified by hand while Yetibot is running.

A much smaller subset of commands need mutable config, e.g.:

- IRC channels
- Room settings

### Prefixes

All immutable config, regardless of the source can be prefixed with either `yb`
or `yetibot`. Examples:

#### edn

```clojure
{:yetibot {:log {:level "debug"}}}
```

```clojure
{:yb {:url "yetibot.com"}}
```

#### Profile

```clojure
{:prod
 {:env
  {:yb-twitter-consumer-key "foo"}}}
```

#### Environment

```bash
YB_GIPHY_KEY="123"
YETIBOT_COMMAND_PREFIX=","
```

#### Merged result

If you decided to configure Yetibot through all available means demonstrated
above (not recommended but shown for purpose of illustration 😅), the merged
config data structure would be:

```clojure
{:log {:level "debug"}
 :command {:prefix ","}
 :url "yetibot.com"
 :twitter {:consumer {:key "foo"}}
 :giphy {:key "123"}}
```

Note how environment variables are exploded into nested maps. This is powered by
[dec](https://github.com/devth/dec) which you can read about in the blog post
[dec: Deep Environmental Config](https://devth.com/2018/dec-deep-environmental-config).

## 🤔

<article class="message is-info">
<div class="message-header">
  <p>Docs didn't answer your question?</p>
</div>
<div class="message-body">
  Ask us in [Slack](https://slack.yetibot.com) or
  [open a new issue](https://github.com/yetibot/community/issues/new)
  on the `community` repo.
</div>
</article>
