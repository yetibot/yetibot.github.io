{:title "Guide: JIRA Basics"
 :layout :post
 :toc true
 :author "@devth"
 :summary "Working with JIRA"
 :tags  ["guide" "2020" "jira"]}


In this [guide](/tags/guide) we cover basic ways of working with the `jira`
command, including:

- creating issues
- updating issues
- assigning issues
- commenting on issues
- logging work on issues
- aliases

Also check out
[Yetibot's JIRA reference](http://localhost:4040/user-guide#jira)
for docs on its full capabilities.

## Channel project

The first thing you'll want to do is set the JIRA project(s) for your channel.
This tells Yetibot the default project to use when running `jira` commands in
your channel, and allows it to auto-expand issues when you mention an issue key
in conversation, without needing to trigger Yetibot manually.

Check current settings:

```yetibot
!channel settings
```

And if `jira-project` is not set, set it with:

```yetibot
!channel set jira-project YETIBOT
```

Once `jira-project` is set we can run commands like `jira recent` to see all
recent tasks for the configured project:

```yetibot
!jira recent
```


Make sure to set `jira-project` for every channel you're in. It can vary from
channel to channel, and also supports multiple comma-separated projects. When
multiple projects are specified, commands like `jira recent` or `jira create`
will default to the first project. `jira-project` also controls a Yetibot
[observer](/user-guide#observers) that listens for words that look like a JIRA
issue key (e.g. `YETIBOt-123`) and returns a quick summary of the issue to
augment a
conversation.

## Create

Let's check the `jira create` docs:

```yetibot
!help jira | grep jira create
```

There are quite a few options, and which ones are required depend on your
particular JIRA project configuration, but `summary` is always required, and
`description` often is. Try it out:

```yetibot
!jira create hello at `time +0` UTC!
```

## Recent issues

We already saw how `jira recent` lists recent issues for the configured projects
in a channel.

```yetibot
!jira recent
```

Internally, this uses JIRA's powerful
[JQL support](https://confluence.atlassian.com/jirasoftwareserver/advanced-searching-939938733.html#Advancedsearching-ConstructingJQLqueries)
to query for issues. With `YETIBOT` as the configured `jira-project`, the exact
query would be:

```
(project in (YETIBOT)) ORDER BY updatedDate
```

This doesn't limit the issues to a certain age, but just returns the most recent
page (default page size is 10) of issues.

## Show

If we know an issue key, we can ask Yetibot to show all of its details:

```yetibot
!jira show YETIBOT-1
```

But what if we just want to show the latest issue without knowing its key? We
can use a combination of commands with pipes, like:

```yetibot
!jira recent | head | jira parse | jira show
```

This works by evaluating commands from left to right, passing the value from one
command to the next across the `|` "pipe" as input:

1. `jira recent` gets the list of recent issues
1. `head` takes the first issue
1. `jira parse` parses out just the issue key, e.g. `YETIBOT-123`
1. `jira show` shows the issue given the key

We'll continue to use this pattern to work on the latest issue throughout the
rest of this guide, so let's [alias](https://yetibot.com/user-guide#aliases) it:

```yetibot
!alias firstjira = "jira recent | head | jira parse"
```

```yetibot
!firstjira
```

## Update

Yetibot can update issues:

```yetibot
!help jira | grep jira update
```

Let's update the description of the most recent issue then pipe it to `jira
show`, which will show us the full description unlike the short format.

```yetibot
!firstjira | jira update %s -d This description was updated at `time +0` UTC | jira parse | jira show
```

<article class="message is-info">
<div class="message-header">
  <p>💡</p>
</div>
<div class="message-body">
  Notice how we used the `%s` symbol above. This instructs Yetibot to substitute
  `%s` with the output from the previous command rather than the default
  behavior of appending to the end. [Read more about Pipes](/user-guide#pipes).
</div>
</article>

You can run this multiple times, and notice the updated timestamp each time it's
run.

## Priority

List all the priorities in JIRA:

```yetibot
!jira priorities
```

When setting a priority in `jira create` or `jira update` use the name, or at
least part of the name, and Yetibot will do its best to match to a known
priority:

```yetibot
!jira update `firstjira` -y med
```

<article class="message is-info">
<div class="message-header">
  <p>💡</p>
</div>
<div class="message-body">
  Notice the use of subexpressions using backticks above. This lets us embed the
  result of an inner command (`firstjira`) into an outer command (`jira
  update`). [Read more about Subexpressions](/user-guide#subexpressions).
</div>
</article>

## Components

List components in JIRA with:

```yetibot
!jira components
```

And just like priorities, we can set the component of an issue:

```yetibot
!jira update `firstjira` -c core | jira parse | jira show
```

Or get crazy and set the component randomly:

```yetibot
!jira update `firstjira` -c `jira components | render {{name}} | random` | jira parse | jira show
```

Try running the above multiple times and see the component change.

## Aliases

We can use [aliases](https://yetibot.com/user-guide#aliases) to further simplify
JIRA issue creation. For example, if we wanted a quick way to create new tasks
assigned to Yetibot, we could alias it with:

```yetibot
!alias yetitask = "jira create $s -a yetibot"
```

Then quickly create new issues for `yetibot` with:

```yetibot
!yetitask do stuff, yeti ⚡️
```

A common use is to hardcode the assignee like above as a fast way to create
issues for yourself. Want to quickly create a list of stuff? Try:

```yetibot
!list fix the foo, deploy the bar, decomplect the baz | xargs yetitask
```

## Assigning issues

Issues can be re-assigned using `jira update`:

```yetibot
!jira recent | head | jira parse | jira update %s -c `jira components | render {{name}} | random` | jira parse | jira show
```

## User search

Search the users in JIRA with:

```yetibot
!jira users yeti
```

## Finally

I hope this guide has helped you increase your automation and Yetibot expression
fluency. While this guide illustrated working with a single command, Yetibot is
well-suited to be the glue between many systems in the communal context of the
mighty **channel**. See [Guide: Google Sheets to JIRA
issues](/2020-04-20-guide-google-sheets-to-jira) for one such reification of
this idea along with more advanced `jira` usage.

If you feel like cleaning up after yourself, use this to delete all the issues
you just created:

```yetibot
!jira jql created > -1h | xargs jira parse | xargs jira delete
```

Question? Ideas for other guides? Post a comment below 🙏.
