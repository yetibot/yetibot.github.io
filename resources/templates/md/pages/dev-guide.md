{:title "Dev Guide"
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

- If you're more interested in using Yetibot, check out the
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
  <p>🚧🏗👷</p>
</div>
<div class="message-body">
These docs are work in progress.
</div>
</article>

## Dev workflow

### Prerequisites

#### Leiningen

Leiningen is the Clojure build tool that Yetibot uses. See the
[Leiningen Installation docs](https://github.com/technomancy/leiningen#installation)
to install it.

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
Slack. See
[Up and running / minimal config](https://yetibot.com/ops-guide/#minimal_config)
docs for a simple IRC example.

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

Building a Yetibot command is easy. The primary interface is `cmd-hook`, which
registers a command with its prefix and set of sub-commands.

Here's an example command that adds 2 numbers:

```clojure
(ns mycompany.plugins.commands.add
  (:require [yetibot.core.hooks :refer [cmd-hook]]))

(defn add-cmd
  "add <number1> <number2> # Add two numbers"
  [{[_ n1 n2] :match}] (+ (read-string n1) (read-string n2)))

(cmd-hook #"add" ;; command prefix
  ;; Pattern to match the subcommand on the left and the function to handle it
  ;; on the right. Notice that we specified a docstring on `add-cmd` - Yetibot
  ;; will use this to populate the help docs for the `add` command.
  #"(\d+)\s+(\d+)" add-cmd)
```

An example invocation would look like:

```
!add 2 3
5
```

And if we ask for help:

```
!help add
add <number1> <number2> # Add two numbers
```

In addition to loading its own internal commands, Yetibot will load all command
namespaces matching:

```clojure
#"^.*plugins\.commands.*"
```

So in our example above, the `mycompany.plugins.commands.add` namespace would be
matched by this pattern and loaded.

For many more examples of various commands, take a look at
[Yetibot's built in commands](https://github.com/yetibot/yetibot/tree/master/src/yetibot/commands).

## Testing yetibot.core changes in yetibot

If you need to test out changes to `yetibot.core` in `yetibot`, this can be done
by installing the `yetibot.core` SNAPSHOT locally and consuming it from
`yetibot`:

```bash
[yetibot.core] $ lein install
Warning: specified :main without including it in :aot.
Implicit AOT of :main will be removed in Leiningen 3.0.0.
If you only need AOT for your uberjar, consider adding :aot :all into your
:uberjar profile instead.
Compiling yetibot.core.init
Created /Users/thartman/oss/yetibot.core/target/yetibot.core-x.y.z-SNAPSHOT.jar
Wrote /Users/thartman/oss/yetibot.core/pom.xml
Installed jar and pom into local repo.
```

Now in `yetibot`'s `project.clj`, set the dependency of `yetibot.core` to:

```bash
[yetibot.core "x.y.z-SNAPSHOT"]
```

Of course you need to replace `x.y.z` with the actual version you're working on.

Make sure to never commit these kind of changes to `master` (assuming they
somehow passed code review). Snapshot versions should only be used during
development.

## Command response structure

The result of a command can be a simple value e.g. a string or collection of
strings. These will be passed directly to the chat adapter to be posted either
as a single message (like the case of a String) or as multiple messages or a
single multi-line message for collections, depending on the capabilities of
the chat adapter. For example, `echo`:

```clojure
(defn echo-cmd
  "echo <text> # Echos back <text>. Useful for piping."
  {:yb/cat #{:util}}
  [{:keys [args]}]
  args)

(cmd-hook #"echo"
  _ echo-cmd)
```

This command simply returns its string args. This was the original behavior of
all commands, but much later we devised a more precise structure that allows
Yetibot to:

1. pass data across pipes and
1. explicitly indicate when an error has occurred.

In the first case (i.e. non error results), a command can return:

```clojure
{:result/value "The formatted string derived from some data"
 :result/data {:the {:data :structure}}}
```

In the second case (i.e. errors), a command should return a `:result/error` key
with an error message string value to indicate that an error took place. This
allows Yetibot to short-circuit pipe expressions early in the face of errors,
making it more clear what happened in an expression:

```clojure
{:result/error "The API blew up"}
```

Let's look at these in more detail.

### Data across pipes

Many commands resolve some sort of data structure through an API call then pull
attributes out of a structure and format them into a human-friendly string. This
is often great from a UX perspective, but we give up so much data in the process
of deriving that string. What if we could have the best of both worlds?

To illustrate the point let's look at a `weather` command:

```yetibot
!weather seattle, wa
```

This is a nice human-friendly representation of the current weather conditions
for Seattle, but how much data are we losing in the process of deriving that
string? Let's peak at the actual data:

```yetibot
!weather seattle, wa | data show
```

That's a lot of data! Since Yetibot passes this data across pipes, we can craft
commands that utilize it in some way. One of Yetibot's built-in commands,
`render`, does exactly that. It allows a user to provide their own formatting
with string templates.

```yetibot
!help render
```

To demonstrate how a user could harness all this data to come up with their own
human-readable derivation (this is the same example taken from the
[user docs](/user-guide#render)):

```yetibot
!weather seattle | render Wind in {{city_name}} at {{wind_spd|multiply:2.23694|double-format:2}} mph blowing {{wind_cdir_full|capitalize}}
```

Check out the source for the `weather` command to see how it works:

```yetibot
!source yetibot.commands.weather/weather-cmd
```

It's not a requirement that your command outputs this structure, but it's highly
recommended!

### Errors

Along the same lines as `:result/data` demonstrated in the previous section, a
command can explicitly return an error by returning a
`{:result/error "error message"}` map. The `weather` command uses this structure
to indicate an invalid location:

```yetibot
!weather bad location
```

```yetibot
!source yetibot.commands.weather/error-response
```

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
  `yetibot.core.handler/handle-unparsed-expr` is called with `chat-source`,
  `user`, and `body`.

### Unparsed expression handling

Raw, unparsed expression are passed to
`yetibot.core.handler/handle-unparsed-expr`, along with the `user` and `body`.
`handle-unparsed-expr` sets a `binding` for the latter 2, then parses and
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
  `yetibot.core.util/pseudo-format`, which is similar to `clojure.core/format`
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

<span class="icon">
  <i class="fab fa-github"></i>
</span>
[Edit this page](https://github.com/yetibot/yetibot.github.io/blob/source/resources/templates/md/pages/dev-guide.md)
