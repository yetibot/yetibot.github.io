{:title "User Guide"
 :subtitle "Welcome to the interactive Yetibot User Guide"
 :layout :page
 :toc true
 :page-index 0
 :navbar? true}

All the examples below are <strong>interactive</strong>. Click the button below
each example evaluate the expression against the live, <a
href="http://public.yetibot.com">public Yetibot instance</a> using the GraphQL
API.

## Basics

This is what a simple command looks like:

```yetibot
!echo hi
```

Yetibot should reply `hi`.

To see a more dynamic example, run `uptime`:

```yetibot
!uptime
```

## Help

The `help` command lets you explore the commands available and their usage. It
has its own help doc:

`!help help`

## Response Types

Yetibot responses are either:

1. A single value
1. A collection of values

There are no other types in Yetibot, though the underlying Clojure data
structures in responses may contain more diverse responses, such as when
returning the result of an API call.

Here's an example of a collection:

```yetibot
!list 1 2 3
```

To view the raw underlying Clojure data structure type of a response in Yetibot,
use `raw`. For example:

```yetibot
!list 1 2 3 | raw
```

## Pipes

Pipes allow chaining together more complex expressions using the output of one
command as the input of another command.

```yetibot
!echo 1 | echo 2 | echo 3
```

Notice how the output of each preceding command is appended to the end of the
following command separated by a space. This is the default behavior, but you
can also choose where to place arguments and control whitespace using `%s`:

```yetibot
!echo foo | echo %sbar
```

## Subexpressions

Subexpressions let you build up more complex expressions by nesting one
expression in another.

```yetibot
!echo `echo Yetibot is` pretty cool
```

Backticks are convenient when you need a single level of nesting, but `$()`
syntax lets you embed any level of nesting:

```yetibot
!echo $(echo $(echo Yetibot) is) alive
```

These examples are necessarily simplistic, but when you start piecing together
more complex commands that fetch data the ability to arbitrarily nest
expressions provides tremendous power.

## Xargs

Xargs allows us to operate over a collection, evaluating an expression for each
value, in parallel.

```yetibot
!help xargs
```

```yetibot
!list 1 2 3 | xargs echo number | unwords
```

## Collection utilities

Since Yetibot can return a collection as a response, it needs basic operations
to manipulate collections.

```yetibot
!help random
```

```yetibot
!help head
```

```yetibot
!help tail
```

```yetibot
!help shuffle
```

There are many others. TODO document them!

## Aliases

Aliases are similar to `alias` in bash allowing us to give a name for a command.

```yetibot
!help alias
```

## Observers

An observer listens for patterns and automatically runs commands when triggered.
They're super powerful but can be easily be abused.

```yetibot
!help observer
```

## Data

Yeibot commands by default return a pretty-printed response for human
consumption, but the underlying data is preserved and accessible as well.

```yetibot
!help data
```

## Cron

Cron is, as you'd expect, a way to run a command on an interval given a cron
expression.

```yetibot
!help cron
```

## Eval

The `eval` command runs arbitrary Clojure against the Yetibot process itself, so
it's by definition very insecure. Because of this, it's only allowed to by run
by users that have been pre-configured to have access.

It can be a fun way of poking at otherwise-unavailable state inside Yetibot.

```yetibot
!help eval
```

## Scrape

```yetibot
!help scrape
```

## GraphQL API

Yetibot serves a GraphQL endpoint as part of its web app. The public Yetibot
instance is accessible at
[https://public.yetibot.com/graphql](https://public.yetibot.com/graphql).

For example, to inspect the configured adapters run a query with a GraphQL
client:

```graphql
{
  adapters {
    uuid
    platform
  }
}
```

