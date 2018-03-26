{:title "Docs"
 :layout :page
 :toc true
 :page-index 0
 :navbar? true}

<strong>Welcome to Yetibot docs!</strong>

Let's walk through a few of the ways in which a user can interact with Yetibot.
All the examples below are <strong>interactive</strong>. Click the button below
each example evaluate the expression against the live, <a
href="http://public.yetibot.com">public Yetibot instance</a> using the GraphQL
API.

## Basics

```yetibot
!echo hi
```

This is what a simple command looks like. Yetibot should reply `hi`.

## Types

Yetibot responses are either:

1. A single value
1. A collection of values

There are no other types in Yetibot, though the underlying Clojure data
structures in responses may contain more diverse responses, such as when
returning the result of an API call.

To view the raw data structure type of a response in Yetibot, use `raw`. For
example:

```yetibot
!list 1 2 3 | raw
```

## Data

Yeibot commands by default return a pretty-printed response for human
consumption, but the underlying data is preserved and accessible as well.

## Pipes

Pipes allow chaining together more complex expressions using the output of one
command as the input of another command.

## Subexpressions

Subexpressions let you build up more complex expressions by nesting one
expression in another.

## Xargs

Xargs allows us to operate over a collection, evaluating an expression for each
value, in parallel.

## Collection utilities

Since Yetibot can return a collection as a response, it needs basic operations
to manipulate collections.

## Aliases

Aliases are similar to `alias` in bash allowing us to give a name for a command.

## Observers

An observer listens for patterns and automatically runs commands when triggered.

## Cron

Cron is, as you'd expect, a way to run a command on an interval given a cron
expression.

## GraphQL API
