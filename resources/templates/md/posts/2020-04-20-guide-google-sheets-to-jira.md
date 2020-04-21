{:title "Guide: Google Sheets to JIRA issues"
 :layout :post
 :toc true
 :author "@devth"
 :summary "Consume a Google Sheet as a CSV and create JIRA issues for each item"
 :tags  ["guide" "2020" "jira"]}

 This guide demonstrates the use of Yetibot to consume a Google Sheet as a CSV
 and create JIRA issues from the rows.

## CSV consumption

 We'll use this
 [Yetibot tasks Google Sheet](https://docs.google.com/spreadsheets/d/1JIp3AjmPIA7T2aJsXPDaz7KxyxJLJGbgkR6r_dpvu_E/edit?usp=sharing).
 To get the sheet in CSV format, just change the end of the URL from
 `edit?usp=sharing` to `export?format=csv`:

```yetibot
!curl https://docs.google.com/spreadsheets/d/1JIp3AjmPIA7T2aJsXPDaz7KxyxJLJGbgkR6r_dpvu_E/export?format=csv
```

We can consume that URL with the `csv` command.

```yetibot
!help csv
```

```yetibot
!csv https://docs.google.com/spreadsheets/d/1JIp3AjmPIA7T2aJsXPDaz7KxyxJLJGbgkR6r_dpvu_E/export?format=csv
```

Let's alias that so it's a little more readable:

```yetibot
!alias yetitasks = "csv https://docs.google.com/spreadsheets/d/1JIp3AjmPIA7T2aJsXPDaz7KxyxJLJGbgkR6r_dpvu_E/export?format=csv"
```

Then make sure it works as expected:

```yetibot
!yetitasks
```

## Towards JIRA

Next, we need to figure out how to pipe that to `jira`.

We can take advantage of the `render` command, which lets us render templates
against a data structure, like the above.

```yetibot
!help render
```

For example, if we only want to look at the `Summary` column:

```yetibot
!yetitasks | render {{Summary}}
```

Let's look at `jira create` docs to see how we can construct it dynamically:

```yetibot
!help jira | grep create
```

So at a minimum, it'd look like:

```yetibot
!yetitasks | render jira create {{Summary}}
```

But we can also take advantage of the other columns:

```yetibot
!yetitasks | render jira create {{Summary}} -d {{Decription}} -t {{Estimate}} -c {{Component}}
```

Finally, to actually run those commands, we can use the `cmd` command:

```yetibot
!help cmd
```

## The tldr

Put it all together:

```yetibot
!yetitasks | render jira create {{Summary}} -d {{Description}} -t {{Estimate}} -c {{Component}} | xargs cmd
```

## 🔥

To clean up we can use `jira jql` to query issues created in the last hour:

```yetibot
!jira jql created > -1h
```

And delete them:

```yetibot
!jira jql created > -1h | xargs jira parse | xargs jira delete
```

🔥

## Power

Hopefully this guide has illustrated the power of `|` pipes, `xargs`, `render`
and `cmd`. They are foundational pieces of Yetibot's expressive pipeline
capabilities.

Have ideas for other guides? Post a comment below!
