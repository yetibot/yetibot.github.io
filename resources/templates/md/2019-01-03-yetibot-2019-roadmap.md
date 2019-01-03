{:title "Looking back at 2018 and forward for 2019"
 :layout :post
 :tags  ["news" "roadmap" "2018" "2019"]}

We made a ton of progress on Yetibot in 2018 and gained some new contributors in
the process! A few high level contributions include:

- launched this site and started a major effort to write comprehensive docs
- added `pagerduty`
- added `catchpoint`
- migrated `weather` to a new API provider
- added `karma`
- added `github releases`
- added support for Slack Reaction-based observers 🤯
- added `gcs` for Google Cloud Storage
- added `cron` command
- created a GraphQL API
- built a new web dashboard and shipped it as
  [`yetibot-dashboard`](https://www.npmjs.com/package/yetibot-dashboard)npm module
- added `render` for custom command output using its `data`
- improved the way we record chat history in the database, including Yetibot's
  own output
- fixed a ton of bugs 😁
- made errors from a command explicit, enabling us to abort a pipeline early
  when there's an error
- improved Slack auto-reconnect
- added ability to reply to threads in Slack

## Contributors in 2018 💥

- [@cheukyin699](https://github.com/cheukyin699)
- [@cvic](https://github.com/cvic)
- [@devth](https://github.com/devth)
- [@gaberger](https://github.com/gaberger)
- [@jcorrado](https://github.com/jcorrado)
- [@kaffein](https://github.com/kaffein)
- [@linuxsoares](https://github.com/linuxsoares)
- [@teodorlu](https://github.com/teodorlu)

## 2019 Roadmap

### Documentation

While we made a great start, the docs are not quite there. This will be a focus
of 2019: continuing to improve coverage of documentation!

For user docs we'll add coverage and examples for more commands, as well as
continue to add more complex examples that showcase some of Yetibot's more
advanced features.

For dev docs we'll improve documentation of Yetibot internals and make it easier
for new contributors to ramp up.

### Web based REPL

We'll work on a truly interactive Yetibot REPL React component and use it on the
docs site so users can more readily play with Yetibot while exploring the docs.

### Data

Toward the end of 2018 we experimented with propagating data behind pipes for
each command. We'll continue exposing data on all commands and play around with
some potential usage before solidifying this potentially superpower feature.

### Configuration

Command configuration in Yetibot is currently spec'd out with schema. We'll move
to `clojure.spec` and start to leverage some of its capabilities for things
like:

- web-based config validation
- config generation (as opposed to a manually maintained and potentially stale
  `config.sample.edn`)
- friendly command output with help docs when a command is not yet configured

### Screencasts

We'll post more screencasts that demonstrate contributing to Yetibot and what an
interactive REPL-based development workflow looks like. We'll try to utilize
Clojure 1.10's new features as well as the more experimental stuff that
Cognitect is putting out, like how REBL fits into our dev workflow.

### And much more

We'll continue to build fun stuff as it comes up, like we've done all along.
Feel free to [join us!](https://slack.yetibot.com)
