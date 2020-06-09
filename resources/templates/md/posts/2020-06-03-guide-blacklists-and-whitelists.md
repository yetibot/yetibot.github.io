{:title "Guide: Blacklists and Whitelists"
 :layout :post
 :toc true
 :author "@devth"
 :summary "Locking down your Yeti with blacklists and whitelists"
 :tags  ["guide" "2020" "ops"]}

Yetibot exposes a plethora of commands ranging from `weather` and `wolfram`
lookups to `meme` generation to `stock` prices to simple text manipulation and
much more. Some operators may not want to expose the full range of Yetibot
capabilities to their users, whether for security, or simplicity, or other
reasons.

<figure>
  ![help](/img/screenshots/help.png)
  <figcaption>`!help` on a Yetibot with many aliases and all commands enabled </figcaption>
</figure>

Now operators can intentionally expose any subset of Yetibot that they'd like
via config. Thanks to [@gkspranger](https://github.com/gkspranger) for helping
us work through this by providing lots of thoughtful feedback and feature
requests! PRs that enabled these changes are:

- [Allow configurable fallback help text #140](https://github.com/yetibot/yetibot.core/pull/140)
- [Exclude aliases from white and black lists #138](https://github.com/yetibot/yetibot.core/pull/138)
- [Fallback to default command handling when a command is disabled #137](https://github.com/yetibot/yetibot.core/pull/137)
- [Exclude help from white black lists #135](https://github.com/yetibot/yetibot.core/pull/135)
- [Add command whitelist/blacklist support #133](https://github.com/yetibot/yetibot.core/pull/133)

## Configuration

When whitelist is configured, all commands are disabled except those present in
the `whitelist` collection, plus any foundational commands. Example config:

```clojure
:yetibot-command-whitelist-0 "echo"
:yetibot-command-whitelist-1 "list"
```

<figure>
  ![help](/img/screenshots/help-whitelist.png)
  <figcaption>`!help` on a Yetibot with a whitelist allowing only `echo` and `list`</figcaption>
</figure>

When blacklist is configured, all commands are enabled except those present in
the `blacklist` collection, plus any foundational commands. Example config:

```clojure
:yetibot-command-blacklist-0 "echo"
:yetibot-command-blacklist-1 "list"
```

<figure>
  ![help](/img/screenshots/help-blacklist.png)
  <figcaption>`!help` on a Yetibot with a blacklist disabling `echo` and `list`</figcaption>
</figure>

## Foundational commands

We intentionally excluded [a few commands](https://github.com/yetibot/yetibot.core/blob/4a32ee3ea46c0aa1f5bb5ffe85057b9323ebc3ed/src/yetibot/core/util/command.clj#L40-L46)
from whitelists and blacklists as they are foundational or could be considered
meta commands:

1. `help` - meta command that lets users know which commands are available, and
   how each command works.
1. `alias` - aliases are all about composing or parameterizing other commands.
1. `channel` - command for working with channel-specific settings.
1. `category` - meta command for working with available commands according to
   their category.

## Customized fallback command

Related to curating the set of available commands, we can also configure the
fallback command (i.e. what happens when a user tries to run a command that
doesn't exist). This example sets it to an alias:

```clojure
:yetibot-default-command "custom"
```

<figure>
  ![help](/img/screenshots/help-custom.png)
  <figcaption>`!help` on a Yetibot with fallback set to a `custom` alias</figcaption>
</figure>

## Customized fallback help docs

In the previous section, notice the output of `!help` includes:

> ✅ Fallback commands are enabled, and the default command is `custom`. This is
> triggered when a user enters a command that does not exist, and passes
> whatever the user entered as args to the fallback command.

This is the default snippet of help text for fallback commands, but this too is
overridable:

```clojure
:yetibot-command-fallback-help-text "Welcome to Yetibot 👋"
```

<figure>
  ![help](/img/screenshots/help-custom-fallback.png)
  <figcaption>`!help` on a Yetibot with custom fallback help text</figcaption>
</figure>
