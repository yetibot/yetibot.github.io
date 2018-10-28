{:title "Developer Guide"
 :subtitle "Welcome to the interactive Yetibot Developer Guide"
 :layout :page
 :toc true
 :page-index 1
 :navbar? true}

 These docs are are work in progress. If something is missing and you have
 questions just ask in #dev channl on [Yetibot Slack](https://slack.yetibot.com).
 Feel free to [open an issue](https://github.com/yetibot/yetibot.github.io/issues)
 to ask questions or suggest changes.

## Running Yetibot locally

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

## Web dashboard
