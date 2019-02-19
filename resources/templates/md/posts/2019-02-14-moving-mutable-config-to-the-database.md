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

