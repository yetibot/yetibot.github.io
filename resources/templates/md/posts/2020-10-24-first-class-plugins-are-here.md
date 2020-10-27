{:title "First class plugins are here!"
 :layout :post
 :toc true
 :author "@devth"
 :tags  ["core" "2020"]}

Since nearly the beginning of its existence, Yetibot has supported the notion of
plugins by simply loading namespaces that looked like commands, e.g.
`mycompany.plugins.commands.mycommand`, but it was up to the user to get the
plugin JAR on the classpath or source file included in the local source tree.

This was never ideal, for a few reasons:

- It meant the user needed to manage all the ops for their custom Yetibot,
  including building (JARs or Docker images) or figuring out a way to deploy
  from a source tree since the official JAR and Docker image were already baked.
- The inconvenience prevented us from embracing a plugin ecosystem, instead
  baking everything into either [yetibot](https://github.com/yetibot/yetibot)
  or [yetibot/core](https://github.com/yetibot/core).

## Usage

Configure the plugins you want to use, and Yetibot will resolve and load them on
start up:

```clojure
{:yetibot
 {:plugins
   {:kroki
     {:artifact "yetibot/kroki"
      :version "20201022.003832.0ae5bf7"}}}}
```

Beware that specifying a large number of plugins will increase Yetibot's start
up time. This is the trade off between static (baking artifacts into an uberjar
or Docker image) and dynamic (loading at runtime on startup).

## Release automation

Yetibot's official plugins (those under the
[Yetibot GitHub Org](https://github.com/yetibot)) are ultra simple to create and
release because of the surrounding automation we constructed:

1. [yetibot/parent](https://github.com/yetibot/parent) uses
   [lein-parent](https://github.com/achin/lein-parent) to specify common
   configuration across all Yetibot plugins (see
   [yetibot-github's `project.clj`](https://github.com/yetibot/yetibot-github/blob/499bc7e902658fdb2461f166af9a6a94a75bd4cb/project.clj#L6-L13)
   for an example of what this looks like).
1. A new Leiningen plugin called
   [lein-inferv](https://github.com/devth/lein-inferv) allows us to infer
   versions rather than specify them in code, which allows us to avoid commit
   automation and noise to bump and snapshot versions. We already practiced this
   in [yetibot/core](https://github.com/yetibot/core) using
   [lein-git-version](https://github.com/arrdem/lein-git-version) but the new
   plugin fully encodes our derived version schema and requires zero
   configuration.
1. [GitHub Organization workflows](https://github.com/yetibot/.github/blob/main/workflow-templates/release.yml)
   let us define how to release plugins in a single place that all future
   plugins can consume.

## How to contribute a new module

If you have an idea for a module and think it should belong under the Yetibot
org as an official plugin, feel free to suggest it in the
[#dev channel on Yetibot Slack](https://slack.yetibot.com).

Otherwise, anyone can build a module wherever they like, release it to an
artifact repository and consume it via configuration.

## [What does it all mean?](https://www.youtube.com/watch?v=MX0D4oZwCsA)

Now that plugins are easy to build, release, and consume, we will move toward
much smaller logically separated code bases. Over time we'll extract commands
from `yetibot` and `yetibot/core` in to separate plugins. This will make
features easier to work with, test in isolation, and release.

[Here's the PR that enabled plugins](https://github.com/yetibot/yetibot.core/pull/153).
The change itself was quite small.

Check out the new [Dynamic plugins docs](/dev-guide#dynamic_plugins), and as
always please give us feedback by leaving a comment below, chatting with us in
[Slack](https://slack.yetibot.com), or opening a GitHub issue.
