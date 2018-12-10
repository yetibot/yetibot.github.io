{:title "Developer Guide"
 :subtitle "Yetibot internals and dev workflows"
 :layout :page
 :toc true
 :page-index 1
 :navbar? true}

<!-- can't indent this properly because Markdown turns it into a code block -->
<article class="message is-info">
<div class="message-header">
  <p>Tip</p>
</div>
<div class="message-body">
  This guide is all about developing Yetibot. It includes docs about dev
  workflow and Yetibot internals.

- If you're more interested using Yetibot, check out the out the
  [User Guide](/user-guide).
- If you're interested in running and operating your own instance of Yetibot,
  check out the [Operations Guide](/ops-guide).
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

<article class="message is-warning">
<div class="message-header">
  <p>🚧🚚👷🏗</p>
</div>
<div class="message-body">
These docs are are work in progress.
</div>
</article>

## Building your first command

## Command pipeline

### Command arguments

Use `raw all` to view arguments.

#### Data

### Push down operations

Yetibot has the ability to look ahead into the command pipeline and optionally
consume subsequent commands from a command handler function. In relational
algebra this is often referred to as pushing down an operation.

Consider `history | random` as an example. The `history` command looks ahead at
the next commands in the pipeline, sees that it's a command it knows how to
consume (`random`), and tells the command execution pipeline to skip it for
efficiency and instead handle itself.

Imagine the default naive method Yetibot would execute if this were not the
case:

1. Load all history into a data structure
1. Pass the data structure to `random` which calls `rand-nth` on the collection.
   According to the [public Yetibot dashboard](https://public.yetibot.com/) at
   the time of writing we have 12,723 entries in the history table. This isn't
   that much but you can imagine how slow it'd be as the table continues to
   grow.

The full set of commands that `history` consumes are defined in
[`yetibot.core.commands.history/consumeables`](https://github.com/yetibot/yetibot.core/blob/f2e045002e20adccb79adbb84eb12566fc99c51e/src/yetibot/core/commands/history.clj#L8):

```clojure
(def consumables #{"head" "tail" "count" "grep" "random"})
```

See [the history command](https://github.com/yetibot/yetibot.core/blob/master/src/yetibot/core/commands/history.clj#L46-L61)
for a full example.

### Timeouts

### Testing commands

1. Using `command-execution-info`
1. Mocking with Midje

## Working with the database

## Parser

## GraphQL API

Yetibot hosts a GraphQL powered API. The public instance is available at
[https://public.yetibot.com/graphql](https://public.yetibot.com/graphql).
Try hitting it with `curl`:

```bash
curl 'https://public.yetibot.com/graphql' \
  -H 'Accept: application/json' \
  --data 'query=%7Beval(expr%3A%20%22uptime%22)%7D' \
  --compressed
```

## Web dashboard

Yetibot hosts a web-based frontend powered by the GraphQL API. See the public
instance at [public.yetibot.com](https://public.yetibot.com).

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
