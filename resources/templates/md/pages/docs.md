{:title "Docs"
 :layout :page
 :toc true
 :page-index 0
 :navbar? true}

## Yetibot Documentation

Welcome to Yetibot docs. Let's walk through a few of the ways in which a user
can interact with Yetibot.

### Basics

```
!echo hi
```

This is what a simple command looks like. Yetibot should reply `hi`.

### Types

Yetibot responses are either:

1. A single value
1. A collection of values

There is no concept of types beyond this. Everything can be treated as a String
conceptually.

To view the raw data structure type of a response in Yetibot, use `raw`. For
example:

```
!list 1 2 3 | raw
```

### Pipes

Pipes allow chaining together more complex expressions using the output of one
command as the input of another command.

### Subexpressions

Subexpressions let you build up more complex expressions by nesting one
expression in another.

### Xargs

Xargs allows us to operate over a collection, evaluating an expression for each
value, in parallel.

### Collection utilities

Since Yetibot can return a collection as a response, it needs basic operations
to manipulate collections.

### Aliases

Aliases are similar to `alias` in bash allowing us to give a name for a command.

### Observers

An observer listens for patterns and automatically runs commands when triggered.

### Cron

Cron is, as you'd expect, a way to run a command on an interval given a cron
expression.
