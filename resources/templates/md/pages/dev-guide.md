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

## Dev workflow

### Prerequisites

#### Leiningen

Leiningen is the Clojure build tool that Yetibot uses. See the [Leiningen
Installation docs](https://github.com/technomancy/leiningen#installation) to
install it.

#### Postgres

Yetibot needs a Postgres database. It defaults to `yetibot` as the database name
(this is configurable). Ensure you have Postgres installed, then create the
database:

```bash
createdb yetibot
```

The default connection string of `postgresql://localhost:5432/yetibot` should
"just work".

#### Configuration

Make sure you've configured at least one chat adapter. This could be IRC or
Slack. See [Up and running / minimal
config](http://localhost:4040/ops-guide/#minimal_config) for a simple IRC
example.

### REPL

Start up a development REPL with:

```bash
lein repl
```

Then run:

```clojure
(start)
```

To load a core set of commands and connect to any configured adapters.

At this point a typical dev workflow would be to iteratively write and reload
code from your editor as is common in the Clojure community. See
[Essentials](http://clojure-doc.org/articles/content.html#essentials) for docs
on setting up various editors for Clojure development.

You can also optionally load all commands from the REPL using:

```clojure
(load-all)
```

To fully reload and restart the adapters and database connections, use:

```clojure
(reset)
```

And to stop, use:

```clojure
(stop)
```

See source for
[`yetibot.core.repl`](https://github.com/yetibot/yetibot.core/blob/master/src/yetibot/core/repl.clj)
for more info.

### Linting

Run this from the repo root to lint:

```bash
codeclimate analyze
```

## Building your first command

## Command handling pipeline

This describes an overview of how yetibot takes raw input and passes it through
its command handling pipeline.

### Raw input

`yetibot.core.handler/handle-raw` is passed params from an adapter:

- `chat-source` e.g. `{:adapter :irc :room "#clojure"}`
- `user` e.g. `{:name devth, :username devth, :id ~devth, :user ~devth, :nick devth}`
- `event-type` one of: `:message`, `:react`, `:leave`, `:enter`, `:sound`, `:kick`
- `body` this is the actual text the user wrote. Only `event-type`s of
  `:message` and `:react` have a `body`. Otherwise it is `nil`. When not `nil`,
  `handle-raw` checks to see if the `body` is prefixed with `!`. If it is,
  `handle-raw` strips the leading `!` and
  `yetibot.core.handler/handle-unprased-expr` is called with `chat-source`,
  `user`, and `body`.

### Unparsed expression handling

Raw, unparsed expression are passed to
`yetibot.core.handler/handle-unprased-expr`, along with the `user` and `body`.
`handle-unprased-expr` sets a `binding` for the latter 2, then parses and
evaluates the expression using `yetibot.core.parser/parse-and-eval`.

### Parsing

`yetibot.core.parser` is an
[Instaparse](https://github.com/Engelberg/instaparse) parser, which fully
specifies the yetibot grammar, including arbitrarily-nested subexpressions,
piped commands and literals. Once a raw expression is parsed into an AST, it is
evaluated using Instaparse's `transform` helper, which takes a map of AST keys
to functions. The important function here is
`yetibot.core.interpreter/handle-expr` which takes any number of individual
commands to be reduced using pipe semantics.

### Evaluating

`handle-expr` literally `reduce`s its `cmds` arguments over the
`yetibot.core.interpreter/pipe-cmds`. Each command is evaluated from left to
right, and each evaluation output is passed as arguments to the next command.
Command output can either be a single value, or a collection of values. This
affects the method `pipe-cmds` will pass it to the next comand:

- **Single value**: `pipe-cmds` will simply append it using
  `yetibot.core.util/psuedo-format`, which is similar to `clojure.core/format`
  except it will append the value at the end of the string if there is not a
  `%s` placeholder present, and if there are *multiple* `%s`s present, it will
  replace *all* of them with the value.
- **Collection**: `pipe-cmds` passes the collection as an optional `:opts` key
  in the `extra` argument to `yetibot.core.interpreter/handle-cmd`, letting
  individual commands do whatever they like with the `:opts`. For example, many
  of the `yetibot.core.commands.collections` commands require a `:opts` key as
  they primarily operate on collections.

`yetibot.core.interpreter/handle-cmd` is the function that gets
[hooked](https://github.com/technomancy/robert-hooke/) by `yetibot.core.hooks`.
Each command in the `yetibot.core.interpreter/hooks` collection gets to look at
the args and decide whether it can handle the input or not. As soon as a single
command handles it, evaluation is complete. If no command handles it,
`handle-cmd` will fallback on google image search.

### Command arguments

Use `raw all` to view all arguments.

```yetibot
!range 3 | raw all
```

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

## Load order

Yetibot loads itself in a particular order. The database should be initialized
and schemas loaded as soon as possible, since many models load themselves based
on it. We want to start logging as soon as possible.

### Database namespaces

All database schemas should live in `db` namespaces:

- `yetibot.db.*`
- `yetibot.core.db.*`
- `*.plugins.db.*`

The `yetibot.core.db` namespace will map over these, building up their `schema`s
if available.

### Logging

`start` fn is called on `yetibot.core.logging` to initialize its
database-appender.

### Chat adapters

Chat adapters are loaded next. Their `start` functions are called, which
connects to the chat protocol and bootstraps its users into the `users` model.

### Observers and commands

Finally, observers and commands are loaded. These typically `require` models and
api namespaces, which may make network or database calls to bootstrap data.

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
