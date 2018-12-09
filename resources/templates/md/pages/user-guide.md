{:title "User Guide"
 :subtitle "Welcome to the interactive Yetibot User Guide"
 :layout :page
 :toc true
 :page-index 0
 :navbar? true}

All the examples below are <strong>interactive</strong>. Click the button below
each example evaluate the expression against the live, <a
href="https://public.yetibot.com">public Yetibot instance</a> using the GraphQL
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

```yetibot
!help help
```

```yetibot
!help
```

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

These examples are necessarily simplistic but when you start piecing together
more complex commands that fetch data, the ability to arbitrarily nest
expressions provides tremendous power.

## Collection utilities

Since Yetibot can return a collection as a response, it needs basic operations
to manipulate collections.

### range

```yetibot
!help range
```

```yetibot
!range 10
```

```yetibot
!range 0 100 25
```

### list

```yetibot
!help list
```

```yetibot
!list Yetibot is alive
```

### xargs

`xargs` allows us to operate over a collection, evaluating an expression for
each value, in parallel.

```yetibot
!help xargs
```

```yetibot
!range 10 | xargs echo number | unwords
```

### random

```yetibot
!help random
```

With no args, random just produces a random number:

```yetibot
!random
```

But if you pass it a collection it takes a random item from it:

```yetibot
!range 10 | random
```

### head

```yetibot
!help head
```

```yetibot
!range 10 | head
```

```yetibot
!range 10 | head 3
```

### tail

```yetibot
!help tail
```

```yetibot
!range 10 | tail 3
```

```yetibot
!range 10 | head 3 | tail
```

### shuffle

```yetibot
!help shuffle
```

```yetibot
!range 10 | shuffle
```

### words

```yetibot
!help words
```

```yetibot
!echo Delta compression using up to 8 threads | words
```

### unwords

```yetibot
!help unwords
```

```yetibot
!range 10 | unwords
```

```yetibot
!echo Delta compression using up to 8 threads | words | shuffle | unwords
```

### join

```yetibot
!help join
```

```yetibot
!range 10 | join
```

```yetibot
!range 10 | join 💥
```

### split

```yetibot
!help split
```

```yetibot
!echo stick-in-the-mud | split -
```

### letters

This is just like `words`, except it splits apart letters.

```yetibot
!help letters
```

```yetibot
!echo Yetibot | letters
```

### unletters

```yetibot
!help unletters
```

```yetibot
!echo Yetibot | letters | shuffle | unletters
```

### trim

```yetibot
!help trim
```

```yetibot
!echo    why such space    | trim
```

### set

```yetibot
!help set
```

```yetibot
!list 1 1 2 2 3 3 | set
```

### count

```yetibot
!help count
```

```yetibot
!range 10 | count
```

### sum

```yetibot
!help sum
```

```yetibot
!range 5 | sum
```

It doesn't like it if you try to sum non-numbers:

```yetibot
!list one two three | sum
```

### sort

```yetibot
!help sort
```

```yetibot
!list foo bar baz | sort
```

### sortnum

```yetibot
!help sortnum
```

```yetibot
!list 22 foos, 33 bars, 11 bazes | sortnum
```

### grep

```yetibot
!help grep
```

```yetibot
!range 50 | grep 5
```

```yetibot
!range 50 | grep -C 1 5
```

### tee

```yetibot
!help tee
```

`tee` doesn't work in the GraphQL API yet, but you can try this out via chat:

```yetibot
!echo foo | tee | echo bar
```

### reverse

```yetibot
!help reverse
```

```yetibot
!range 3 | reverse
```

### droplast

```yetibot
!help droplast
```

```yetibot
!list first middle last | droplast
```

### rest

```yetibot
!help rest
```

```yetibot
!range 10 | rest
```

### Other collection commands

There are a few others not documented here such as `raw`, `keys`, vals`, and
`data` (which is documented in its own section of this guide). To view them all
we can look them up by category:

```yetibot
!category list collection
```

## Aliases

Aliases are similar to `alias` in bash allowing us to give a name for a command.
This is typically a heavily-used feature as teams build up aliases for fun or
utility and become a manifestation of culture.

```yetibot
!help alias
```

## Observers

An observer listens for patterns and automatically runs commands when triggered.
They're super powerful but can be easily be abused.

```yetibot
!help observer
```

Run the above help docs. As you can see, observers support several different
event types.

### message

The default event type for observes is `message`. This allows Yetibot to react
to a message by running a command. For example:

```yetibot
!obs sushi = react :sushi:
```

With this observer any time anyone mention sushi they get a 🍣 reaction. Note
that we could have specified a regex pattern instead of the literal "sushi".

It also supports optional settings that let you filter on:

- the name of the channel using `-c`
- the username of the person who posted a message using `-u`

For example:

```yetibot
!obs -c dev-testing -u devth = echo {{username}} said {{body}} in {{channel}}
```

The above example also illustrates the templating functionality. Along with
`username` and `body`, `channel` is available on all event types, and for
`react` observer events, `reaction` and `message-username` are also available.

### react

A `react` event fires when a user reacts to a message (Slack only).

```yetibot
!obs -c dev-testing -e react = giphy {{reaction}} {{body}}
```

This causes a giphy lookup using the reaction used (e.g. `100` or `smile`) and
the body text of the message that was reacted to.

React events also have two other fields available: `reaction` and
`message-username` where `message-username` is the username of the user that
posted the original message (`username` is the `username` of the user that
reacted).

### enter

The `enter` event fires when a user enters a channel.

```yetibot
!obs -c dev-testing -e enter = meme internet: welcome to {{channe}} {{username}}!
```

### leave

The `leave` event fires when a user leaves a channel.

```yetibot
!obs -c dev-testing -e leave = meme crying jordan: / bye {{username}}
```

## Data

Yetibot commands by default return a pretty-printed response for human
consumption, but for many commands the underlying data is preserved and passed
across the pipe as well:

```yetibot
!help data
```

For example, we can get all the data behind the `weather` command:

```yetibot
!weather seattle, wa | data show
```

## Cron

Cron is, as you'd expect, a way to run a command on an interval given a cron
expression.

```yetibot
!help cron
```

## Eval

The `eval` command runs arbitrary Clojure against the Yetibot process itself, so
it's by definition very insecure. Because of this, it's only allowed to be run
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

For example, to inspect the configured adapters, run the following query with a GraphQL
client:

```graphql
{
  adapters {
    uuid
    platform
  }
}
```

## Examples

### Alltemps

We use an alias to store the list of zip codes for all members of our
distributed team, which we then feed to another alias which outputs a short
single-line description of current weather for a location.

```
!alias locs = list 59101 98101 94101

!alias loctemp = "weather $s | xargs sed s/Current conditions for / | head 2 | reverse | unwords"

!alias alltemps = "locs | xargs loctemp | sort"

!alltemps

25.4 F (-3.7 C), Mostly Cloudy Jupiter Sulphur, Billings, Montana elevation 3114 ft:
43.2 F (6.2 C), Partly Cloudy Belltown, Seattle, Washington elevation 135 ft:
49.8 F (9.9 C), Overcast SOMA - Near Van Ness, San Francisco, California elevation 49 ft:
```

### Yetibot should not have kids

I'm pretty fond of this one. I ~~needed~~ *really wanted* a way to seed a meme
alias with valid sentences like:

> [user] should not [do something]

Time for some Google Complete, JavaScript, and a few aliases!

First, we need a random letter to seed Google Complete with, for ultimate
variety of "shoulds":

```
!alias randletter = "range 65 91 | xargs echo | random | js String.fromCharCode(%s)"

!repeat 5 randletter | unwords

V L R U S
```

LGTM! ☝️

Now pipe that to a well-crafted `complete` query:

```
!randletter | complete should i | random | sed s/should i/

invest in bonds
```

Awesome, let's alias it:

```
!alias randshould = "randletter | complete should i | random | sed s/should i/"

!repeat 10 randshould

take creatine
call her
max out my 401k
move to san francisco
shave my beard
have kids
buy a house
do it
feed feral cats
have a savings account
```

Finally:

```
!alias usershouldnot = "user | random | echo %s should not `randshould`"

!usershouldnot | meme angry wolf:
```

![yetibot should not](//i.imgflip.com/wx53f.jpg)

👏

### Grids

```
!alias dis = echo ಠ_ಠ

!alias grid = "repeat 3 echo $(repeat 3 echo $s | unwords)"

!grid `dis`

ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ

!grid `dis` | xargs grid

ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ

!grid `dis` | xargs grid | xargs xargs grid

ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ ಠ_ಠ
```

I think you get the idea 🧐

### Hide yo

```
!alias hide = "meme hide yo: hide yo /"
!list wife, kids, husband too | xargs hide | unwords
```

![hide yo wife](//i.imgflip.com/wx1cd.jpg "hide yo wife")
![hide yo kids](//i.imgflip.com/wx1cb.jpg "hide yo kids")
![hide yo husband too](//i.imgflip.com/wx1cc.jpg "hide yo husband too")
