# Yetibot workshop

## Agenda

- Yetibot usage fundamentals
- Livecode a Yetibot feature with the REPL
- Clojure language basics
- Resources for getting started
- Open time for questions, play, hacking on Yetibot

 Yetibot usage fundamentals

Instead of working through Yetibot's primitives and its many individual
capabilities we'll start with a non trivial expression that's made up of several
levels of nested aliases composed of piped commands. This will better illustrate
how such primitives can be combined into something ~useful~ fun.

```
!repeat 5 yetishould
```

To start unpacking this we can use `help`:

```
!help yetishould
```

Help shows us that it's an alias for an expression:

`TODO` - allow multiline yetibot expressions

```
list batman insanity kahn gasp
  | random
  | meme %s: yetibot
    `list should, should not, must, must not | random`
    `randshould`
```

Out of the commands in that expression we can see:

1. list used to build up a list of memes
1. random to select a random meme from the list
1. meme to generate a meme
1. sub expression to randomly choose from "should", "should not", "must" and
   "must not
1. randshould, which is itself an alias.

Let's unpack `randshould`:

```
!help randshould
randshould # alias for randletter | complete should i | random | sed s/should i/ | trim
```

Unpack its contents:

```
!help randletter
randletter # alias for range 65 91 | xargs echo | random | js String.fromCharCode(%s)
```

Finally we have expanded all the way down to built in commands. Let's take a
look at each one:

```
!help range
range <end> # create a list from 0 to <end> (exclusive)
range <start> <end> # create a list from <start> (inclusive) to <end> (exclusive)
range <start> <end> <step> # create a list from <start> (inclusive) to <end> (exclusive) by <step>

Examples:
range 2 => 0 1
range 2 4 => 2 3
range 0 6 2 => 0 2 4

Results are returned as collections.
```

```
!help xargs
xargs <cmd> <list> # run <cmd> for every item in <list> in parallel; behavior is
similar to xargs(1)'s xargs -n1
```

```
!help random
random <list> # returns a random item from <list>
random # generate a random number
```

```
!help sed

sed s/<search-pattern>/<replace-pattern> <string> # replace <search-pattern>
with <replace-pattern> on piped contents

sed s/<search-pattern/ <string> # replace <search-pattern> with nothing on piped
contents
```





### Values

At its most basic level, Yetibot takes a command and outputs a response.

```
!echo ebay
```

### Pipes

Pipes let us compose the output from multiple commands in a series to a single
response:

```
!echo ebay | echo are | echo we
```

### Subexpressions

We can also embed commands with sub expressions:

```
!echo we $(echo are $(echo ebay))
```

### Collections

A Yetibot response can be a collection of values instead of a single value.
Yetibot will output each item in the collection on its own line.

The list command builds a collection using space or comma-separated items:

```
!list one two three
!list this is, also a collection
```

### Custom rendering of data

One of the more interesting recent concepts in Yetibot is data behind pipes.

Data and
render

### Aliases

As we've seen, Yetibot commands can be quite expressive, but as they grow in
complexity they become harder to invoke. This is where aliases come in.
