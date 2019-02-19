{:title "Moving mutable configuration to the database"
 :layout :post
 :tags  ["news" "2019" "config"]}


It's time to move [mutable config](https://yetibot.com/ops-guide#mutable) to the
database. Why?
[Immutable infrastructure](https://www.digitalocean.com/community/tutorials/what-is-immutable-infrastructure).

Yetibot embraces
[modern infrastructure](https://devth.com/2018/dec-deep-environmental-config)
best practices. We made a lot of progress moving to mostly-immutable
configuration. This is the next step.

One reason why we haven't done this up till now is that mutable config has never
been relied upon much. You can do things like configure per-channel settings
with the `channel` command. These are then persisted to a local edn file. This
is not durable at all. In an environment like Kubernetes this would be lost on
each pod creation (unless a durable disk was mounted, but that's a pain). We
already have a durable place to store keys and values: the Postgres database.

## What does this mean for me?

Given that mutable config hasn't been heavily used the migration should be quite
painless. We are not providing an automated migration tool, so your options are:

1. Look in `config/mutable.edn` and manually copy the key/values and chat source
   rooms to the postgres table. For example, if your `mutable.edn` looks like:

   ```edn
   :room
   {:ybslack
    {"#obs" {"broadcast" "false"}, "local" {"jira-project" "YETIBOT"}}}}
   ```

   You would create rows:

  | chat-source-adapter | chat-source-room | key          | value   |
  |---------------------|------------------|--------------|---------|
  | :ybslack            | #obs             | broadcast    | false   |
  | :ybslack            | local            | jira-project | YETIBOT |
  |                     |                  |              |         |

1. Use Yetibot to recreate the config, e.g. `channel set jia-project myjira`

1. Do nothing 😅
