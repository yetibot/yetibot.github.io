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

A little more dynamic example:

```yetibot
!uptime
```

## Types

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

To view the raw data structure type of a response in Yetibot, use `raw`. For
example:

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
!list 1 2 3 | xargs echo number | unwords
```

## Collection utilities

Since Yetibot can return a collection as a response, it needs basic operations
to manipulate collections.

## Aliases

Aliases are similar to `alias` in bash allowing us to give a name for a command.

## Observers

An observer listens for patterns and automatically runs commands when triggered.

## Data

Yeibot commands by default return a pretty-printed response for human
consumption, but the underlying data is preserved and accessible as well.


## Cron

Cron is, as you'd expect, a way to run a command on an interval given a cron
expression.

## GraphQL API
