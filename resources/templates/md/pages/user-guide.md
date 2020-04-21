{:title "User Guide"
 :subtitle "Interactive guide to using your Yetibot"
 :layout :page
 :toc true
 :page-index 0
 :navbar? true}

<!-- can't indent this properly because Markdown turns it into a code block -->
<article class="message is-info">
<div class="message-header">
  <p>Tip</p>
</div>
<div class="message-body">
  This guide is all about interacting with Yetibot from the user's
  perspective. It documents runtime usage and many of the available commands.

- If you're more interested in Yetibot's internals or building features, check
  out the [Developer Guide](/dev-guide).
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

All the examples below are <strong>interactive</strong>. Click the button below
each example evaluate the expression against the live, <a
href="https://public.yetibot.com">public Yetibot instance</a> using the <a
href="#graphql_api">GraphQL API</a>.

## Basic Yetibot expressions

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
!echo `echo Hello` Yetibot
```

Backticks are convenient when you need a single level of nesting, but `$()`
syntax lets you embed any level of nesting:

```yetibot
!echo $(echo $(echo Yetibot) is) `echo alive`
```

These examples are necessarily simplistic but when you start piecing together
more complex commands that fetch data, the ability to arbitrarily nest
expressions is quite useful.

## Fun 🎉

Fun has always been an important part of Yetibot's existence. The full list of
commands in the `fun` category can be listed via:

```yetibot
!category list fun
```

Below we document a few highlights.

### Meme generation

Meme gen was one of Yetibot's first features 😂.

```yetibot
!meme yetibot: hello world!
```

```yetibot
!help meme
```

```yetibot
!catfact | meme
```

```yetibot
!chuck | meme chuck:
```

```yetibot
!jargon | meme yeah if you:
```

### Giphy

```yetibot
!help giphy
```

```yetibot
!giphy reaction
```

```yetibot
!giphy whoa
```

```yetibot
!giphy random
```

```yetibot
!giphy trending
```

### No

```yetibot
!help no
```

```yetibot
!no
```

### Http

```yetibot
!http 404
```

```yetibot
!http 200
```

```yetibot
!http 401
```

```yetibot
!http 500
```

```yetibot
!http 420
```

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

As an example, look at the default output of `stock`:

```yetibot
stock tsla
```


## Observers

An observer listens for patterns and automatically runs commands when triggered.
They're super powerful but can easily be abused.

```yetibot
!help observer
```

Run the above help docs. As you can see, observers support several different
event types.

### message

The default event type for observers is `message`. This allows Yetibot to react
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

## Categories

Yetibot commands can be organized under categories. Commands can be enabled or
disabled according to channel settings (e.g. `:fun`). In the future, `help` might
rely on categories.

Categories are stored as meta-data directly on command handler functions under a
`:yb/cat` prefix with a `Set` of keywords as the value.

Current known categories are as follows. Please add to this list as needed. Some
categories will overlap but are semantically distinct.

```yetibot
!help category
```

```yetibot
!category
```

```yetibot
!category list fun
```

```yetibot
!category list util
```

```yetibot
!category list repl
```

### Channel-based category toggle

Each category can be disabled or enabled at the channel level. By default all
categories are enabled. To disable them, use:

```
!category disable :category-name
```

<article class="message is-info">
<div class="message-header">
  <p>NB</p>
</div>
<div class="message-body">
  Disabled categories are stored using the normal channel settings, so you'll
  see them in `!room` if you set them. `!category` is merely a convenience
  wrapper.
</div>
</article>

Show the list of categories and their docs:

```yetibot
!category
```

Disable the "fun" category:

```
!category disable fun
```

Re-enable it:

```
!category enable fun
```

## SSH

Yetibot can `ssh` into servers and run commands on your behalf.

The config looks like:

```clojure
{:yetibot
 {;; ...

  :ssh {:groups
        [{:user "",
          :servers [{:host "", :name ""} {:host "", :name ""}],
          :key "path-to-key"}]},
 }}
```

Each map inside the `:groups` collection has a single `user` and `key` and
allows multiple servers.

For example, if we had a server with name `example` we could see it in the list
of servers via:

```
!ssh servers
```

and run commands via:

```
!ssh example echo foo
```

Yetibot `ssh` currently only supports key-based authentication.

<article class="message is-info">
<div class="message-header">
  <p>Note</p>
</div>
<div class="message-body">
  See full [config docs](/ops-guide#configuration).
</div>
</article>

## Utilities

### Data

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

### Render

The `render` command lets us turn the data discussed in the previous section
into strings, which means we can customize the output of a command using the
data behind it!

Using our `weather` example again:

```yetibot
!weather seattle | render Wind in {{city_name}} at {{wind_spd|multiply:2.23694|double-format:2}} mph blowing {{wind_cdir_full|capitalize}}
```

The templating support is provided by
[Selmer](https://github.com/yogthos/Selmer). It supports a number of filters,
e.g. `{{name|capitalize}}`. See the
[Selmer docs](https://github.com/yogthos/Selmer#usage) for more!

Need to know the ID of the `computer gandalf` meme for some reason?

```yetibot
!meme search computer gandalf | data show
```

```yetibot
!meme search computer gandalf | render ID of {{name}} at {{url}} is {{id}}
```

We could go on and on (and on and on). `render` opens up a ton of possabilities
for customizing command output and using Yetibot in unexpected and unanticipated
ways!

### Cron

Cron is, as you'd expect, a way to run a command on an interval given a cron
expression.

```yetibot
!help cron
```

### Eval

The `eval` command runs arbitrary Clojure against the Yetibot process itself, so
it's by definition very insecure. Because of this, it's only allowed to be run
by users that have been pre-configured to have access.

It can be a fun way of poking at otherwise-unavailable state inside Yetibot.

```yetibot
!help eval
```

### Scrape

```yetibot
!help scrape
```

### Channel settings

Arbitrary key/value pairs can be stored on a per-channel basis. This lets you do
things like set channel local JIRA projects, Jenkins jobs, or other values that
could for example be utilized by aliases.

```yetibot
!help channel
```

### That

The `that` command retrieves the last non-command thing said, excluding Yetibot
output, and `that cmd` retrieves the last command.

```yetibot
!help that
```

Example usage:

```
!that | meme insanity:
```

## Karma

The `karma` command lets you increment or decrement another user's karma along
with an optional note.

```yetibot
!help karma
```

View the leaderboard:

```yetibot
!karma
```

There are three ways to adjust a user's Karma.

The canonical `!karma` command invocation, using the traditional C increment (`++`) or decrement (`--`) operators, optionally followed by a note.

```yetibot
!karma @yetibot++ thanks Yetibot
```

```yetibot
!karma @yetibot-- you had one job
```

The Emoji versions to add (🌈) or subtract (⛈), optionally followed by a note.

```plain
🌈 @yetibot
```

```plain
⛈ @yetibot I told you to go before we got in the car!
```

Via Emoji reactions, which necessarily preclude the addition of notes.

![karma screenshot](/img/screenshots/karma.png)

At this time removing your Emoji reaction does not reverse the initial addition or subtraction of Karma.

In all cases, Yetibot will respond with the user's new score.  Emoji reaction Karma is reported in a thread.

Now take a look at Yetibot's Karma:

```yetibot
!karma @yetibot
```

In addition to these commands, `karma` is also exposed via the GraphQL API!

Try a query like:

```bash
# scores
curl -s 'https://public.yetibot.com/graphql' \
  -H 'Accept: application/json' \
  --data 'query={karmas(report: SCORES) {user_id score}}' \
  --compressed | jq

# givers
curl -s 'https://public.yetibot.com/graphql' \
  -H 'Accept: application/json' \
  --data 'query={karmas(report: GIVERS) {user_id score}}' \
  --compressed | jq

# inspect Yetibot's karma
curl -s 'https://public.yetibot.com/graphql' \
  -H 'Accept: application/json' \
  --data 'query={user(id:"U3K6P707R"){username,karma}}' \
  --compressed | jq

```

You can configure the positive and negative Emojis used in commands and reactions, overriding the default 🌈 and ⛈.  Have a look at [config/config.sample.edn](https://github.com/yetibot/yetibot.core/blob/master/config/config.sample.edn).

Please use Slack shortcodes and not the Unicode characters themselves.

```edn
:karma {:emoji {:positive ":taco:" :negative ":poop:"}}}}
```


## GitHub

```yetibot
!help gh
```

List the open PRs for Yetibot:

```yetibot
!gh pr yetibot
```

or try Clojure:

```yetibot
!gh pr clojure
```

List Yetibot's repos:

```yetibot
!gh repos yetibot
```

List the tags on `yetibot.core`:

```yetibot
!gh tags yetibot/yetibot.core
```

List contributors on the `yetibot/yetibot` repo since last month:

```yetibot
!gh contributors yetibot/yetibot since 1 month ago
```

Look up git change stats on Clojure:

```yetibot
!gh stats clojure/clojure
```

Look up git change stats on Yetibot's first 3 repos:

```yetibot
!gh repos yetibot | head 3
```

```yetibot
!gh repos yetibot | head 3 | xargs words | xargs head | xargs gh stats
```

## JIRA

Yetibot's JIRA capabilities are pretty powerful, especially when combined with
Yetibot's expressions pipeline capabilities. It can operate over a global list
of projects or per-channel project settings. Operations include creating,
updating, resolving, describing, deleting, assigning, logging work, and
commenting on issues.

It can also search issues using JIRA's powerful
[`jql`](https://confluence.atlassian.com/jiracore/blog/2015/07/search-jira-like-a-boss-with-jql)
syntax.

```yetibot
!help jira
```

### JIRA Basics

Let's start by creating a new issue:

```yetibot
!jira create new issue from yetibot.com!
```

If we list recent issues and you should see the issue you just created at the
top:

```yetibot
!jira recent
```

We can get more details on that issue:

```yetibot
!jira recent | head | jira parse | jira show
```

Let's break this down keeping in mind values flow across `|` pipes:

1. `jira recent` - list the recent issues
1. `head` - take the first issue from the list
1. `jira parse` - extract the issue key from a url, e.g. extract `YETIBOT-X`
   from `https://yetibot.atlassian.net/browse/YETIBOT-X`
1. `jira show` - describe the issue

If we knew the issue key ahead of time, we could have simply used it:

```yetibot
!jira show YETIBOT-4
```

We could also parse issue keys out of all recent issues via:

```yetibot
!jira recent | xargs jira parse
```

What if you want to create a subtask? We can do that too using the `-p` option
to specify the parent when creating:

```yetibot
!help jira | grep create
```

Create a sub-task of our most recent issue:

```yetibot
!jira recent | head | jira parse | jira create I am a subtask -p %s
```

### JIRA JQL

If you want to quickly search for issues:

```yetibot
!jira search demo
```

This runs a JQL query that looks like:

```
project in (YETIBOT) AND
  (summary ~ "demo" OR description ~ "demo" OR comment ~ "demo")
```

It searches across 3 fields:

1. `summary`
1. `description`
1. `comment`

But you can also drop down to raw JQL when the need arises:

```yetibot
!jira jql created >= "-5h"
```

Checkout
[Atlassian's Advanced searching docs](https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html)
and
[Advanced searching - operators reference](https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-operators-reference-764478341.html)
for more info on using JQL. It's super powerful.

### Get fancy with JIRA

Let's look at some of the ways we can interact with our issue with the power of
Yetibot expressions.

```yetibot
!jira recent | head | jira parse | jira comment %s Works on my machine
```

We can also assign issues, but first let's see who's all available:

```yetibot
!jira project-users
```

Note: we can also search for users, system wide:

```yetibot
!jira users t
```

```yetibot
!jira users t | data show
```

Assign a random issue to a random user (try running this multiple times for
extra chaos 😈):

```yetibot
!jira recent | random | jira parse | jira assign %s `jira project-users | random`
```

Or assign all issues that mention `docs` in the summary to Yetibot:

```yetibot
!jira jql summary ~ docs | xargs jira parse | xargs jira assign %s Yetibot
```

Let's add a worklog item:

```yetibot
!jira recent | random | jira parse | jira worklog %s 15m explored the docs
```

### Components, versions, issue types, projects

List components:

```yetibot
!jira components
```

All of the JIRA commands expose data. For example, take a peek at the full API
response for a component:

```yetibot
!jira components | head | data show
```

This gives us flexability to get at any piece of the data that might not be
included in Yetibot's default formatted output. What if we wanted to get the
avatar of the first component's lead?

```yetibot
!jira components | head | render {{lead.avatarUrls.48x48}}
```

We can also list things like versions, issue types, and projects:

```yetibot
!jira versions
```

```yetibot
!jira issue-types
```

```yetibot
!jira projects
```

Search for projects matching `yet`:

```yetibot
!jira projects yet
```

Peek at some raw data behind the pipe:

```yetibot
!jira projects | random | data show
```

We can combine any of these with Yetibot's pipeline capabilities and do batch
operations.

### JIRA batch combos

```yetibot
!list do the right thing, do the best thing, do the fastest thing | xargs jira create
```

```yetibot
!jira jql summary ~ thing AND resolution = Unresolved
```

```yetibot
!jira jql summary ~ thing AND resolution = Unresolved | random | jira parse | jira comment %s I `list agree,disagree | random`
```

Batch resolve all the `thing`s:

```yetibot
!jira jql summary ~ thing AND resolution = Unresolved | xargs render {{key}}
```

```yetibot
!jira jql summary ~ thing AND resolution = Unresolved | xargs render {{key}} | xargs jira resolve %s Fixed
```

Now clean your JIRA with `jira delete`:

```yetibot
!jira jql summary ~ thing AND resolution = Done | xargs jira parse | xargs jira delete
```

🔥


And if you want to *really* clean up, delete all issues created today:

```yetibot
!jira jql created >= startOfDay()
```

```yetibot
!jira jql created >= startOfDay() | xargs jira parse | xargs jira delete
```

🔥😑

### JIRA Configuration

JIRA configuration looks like:

```edn
  :jira {:default {:project {:key "Optional"}, :issue {:type {:id "3"}}},
         :user "",
         :projects [{:default {:version {:id "42"}}, :key "FOO"}],
         :subtask {:issue {:type {:id "27"}}},
         :domain "",
         :password ""},
```

The `projects` key is optional and specifies the global list of projects. This
is mostly important for the observer that detects a JIRA task like `PROJ-123`
and auto outputs the details of the task, when found.

This ability is also configurable on a per-channel basis using
[channel settings](#channel_settings):

```
!channel set jira-project YETIBOT,COM
```

After setting that in a channel, Yetibot will know to expand all occurrences of
strings that look like JIRA keys, such as `YETIBOT-123` or `COM-2`.

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

Or if you prefer examples in `curl`:

```bash
# list the configured Adapters
curl -s 'https://public.yetibot.com/graphql' \
  -H 'Accept: application/json' \
  --data 'query={adapters {uuid platform}}' \
  --compressed | jq

# get some stats about this Yetibot
curl -s 'https://public.yetibot.com/graphql' \
  -H 'Accept: application/json' \
  --data 'query={stats {uptime adapter_count user_count command_count}}' \
  --compressed | jq
```

## Recipes

These recipes are fun example usages of Yetibot that more holistically
communicate its capabilities and historical usage.

### Celcius / Fahrenheit conversion with render

The built in `render` command is quite powerful because it uses the
[Selmer library](https://github.com/yogthos/Selmer) for rendering
templates, which includes many
[filters](https://github.com/yogthos/Selmer#filters) for postprocessing a value.

The following example illustrates this by implementing Celcius to Fahrenheit
conversion, and vice versa, in terms of `render`:

```
!alias ctof = "echo $s°C = `render {{$s|multiply:1.8|add:32|round}}°F`"
!alias ftoc = "echo $s°F = `render {{$s|add:-32|multiply:5|divide:9|round}}°C`"
```

```yetibot
!ctof 0
```

```yetibot
!ftoc 100
```

### Countdown

This alias uses JavaScript to determine the number of days till a specific date
and outputs the day along with a string message. It could be further abstracted
as a `countdown` alias that takes a date and a message, but we typically just
re-define the alias as needed.

```
!alias countdown = "js Math.ceil((Date.parse('4/2/2019') - Date.now()) / (1000 * 60 * 60 * 24)) + ' days until Google+ shutdown'"
```

```yetibot
!countdown
```

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

Or try the variant, `yetishould`:

```yetibot
!yetishould
```

Hint: run it more than once 😁

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
[Edit this page](https://github.com/yetibot/yetibot.github.io/blob/source/resources/templates/md/pages/user-guide.md)
