In the latest release, `0.5.31` we focused on power-ups to history across all
surfaces:

- `history` command
- GraphQL `history` resource
- web dashboard

As well as new `date` and `duckling` commands that make it easy to express a
date with natural language to support `history`'s new `--since` and `--until`
options.

These improvements give the user much more precision in browsing or searching
through chat history by providing options to filter on:

- user
- channel
- since date
- until date

as well as options to exclude:

- commands
- non-commands
- yetibot responses

and an option to include `history` commands (it's excluded by default).

This can be used for all kinds of fun and useful spelunking through past usage
and conversation.


```
"history # show chat history

 By default all history except for `history` commands are not included, since
 they make it too easy for a history command to query itself.

 To include them, use:

 -h --include-history-commands

 To further specify which types of history is excluded use any combination of
 these options:

 -y --exclude-yetibot - excludes yetibot responses
 -c --exclude-commands - excludes command requests by users
 -n --exclude-non-commands - excludes normal chat by users

 For example, to only fetch Yetibot responses:

 history -cn

 To only fetch commands:

 history -ny

 To only fetch non-Yetibot history:

 history -nc

 By default history will only fetch history for the channel that it was
 requested from, but it can also fetch history across all channels within a chat
 source by specifying:

 -a --include-all

 You can also specify a channel or channels (comma separated):

 -c --channels

 For example:

 history -c #general,#random

 Search history from a specific user:

 -u --user

 For example:

 history -u devth

 Search within a specific date range:

 -s --since <date>
 -v --until <date>

 Note: <date> can be specified in a variety of formats, such as:

 - 2018-01-01
 - 2 months ago
 - 2 hours ago

 It uses duckling to parse these from natural language.

 history can be combined with pipes as usual, but it has special support for a
 few collection commands where it will bake the expression into a single SQL
 query instead of trying to naively evaluate in memory:

 history | grep <query> - uses Postgres' ~ operator to search
 history | tail [<n>] - uses LIMIT n and ORDER_BY
 history | head [<n>] - uses LIMIT n and ORDER_BY
 history | random - uses LIMIT 1 Postgres' ORDER_BY random()
 history | count - uses COUNT(*)
 "
```

## Examples
