{:title "Moving mutable configuration to the database"
 :layout :post
 :author "@devth"
 :toc true
 :tags  ["news" "2019" "config"]}


It's time to move [mutable config](https://yetibot.com/ops-guide#mutable) to the
database in adherence with
[immutable infrastructure](https://www.digitalocean.com/community/tutorials/what-is-immutable-infrastructure)
practices. Yetibot embraces [modern infrastructure](https://devth.com/2018/dec-deep-environmental-config). We made a
lot of progress moving to mostly-immutable configuration. This is the next step,
and is done as of Yetibot `0.5.0`.

One reason why we haven't done this up till now is that mutable config has never
been relied upon much. Its purpose was to:

1. Store channel-specific configuration (e.g. `jira-project`, `broadcast`,
   `jenkins-default` or any other arbitrary room-specific key/value) for the
   `channel` command
1. Store channel-specific disabled categories for the `category` command
1. Remember which channels Yetibot should join upon connecting to IRC

Previously these values would be persisted to a local edn file which by default
lives at `config/mutable.edn`. However, in modern cloud environments this is not
durable. For example when running Yetibot on Kubernetes this would be lost on
each pod creation (unless a durable disk was mounted, but that's an unnecessary
complication). We already have a durable place to store keys and values: the
Postgres database.

All of these use cases will now move to a single `yetibot_channels` table.

## What does this mean for me?

Given that mutable config hasn't been heavily used the migration should be quite
painless. We are not providing an automated migration tool, so your options are:

1. Do nothing if you're not using any mutable config yet (quite likely) 😅
1. Use Yetibot to recreate the config, e.g. `channel set jia-project myjira`
1. Look in `config/mutable.edn` and manually copy the key/values and chat source
   rooms to the `yetibot_channels` Postgres table. For example, if your
   `mutable.edn` looks like:

   ```edn
   {:room
    {:ybslack
     {"#general" {:disabled-categories #{:crude}},
      "#dev" {"jira-project" "YETIBOT",
              "nope" "lol",
              :disabled-categories #{:crude}}}}}
   ```

   You would create rows in `yetibot_channels`:

<table>
<tr>
  <th>`chat_source_adapter`</th>
  <th>`chat_source_room`</th>
  <th>`key`</th>
  <th>`value`</th>
</tr>
<tr>
  <td>:ybslack</td>
  <td>#general</td>
  <td>disabled-categories</td>
  <td>#{:crude}</td>
</tr>
<tr>
  <td>:ybslack</td>
  <td>#dev</td>
  <td>jira-project</td>
  <td>YETIBOT</td>
</tr>
<tr>
  <td>:ybslack</td>
  <td>#dev</td>
  <td>nope</td>
  <td>lol</td>
</tr>
<tr>
  <td>:ybslack</td>
  <td>#dev</td>
  <td>disabled-categories</td>
  <td>#{:crude}</td>
</tr>

</table>

All values in the table are strings.

If you use IRC, your channels to join config will be lost as well. Simply
re-invite Yetibot to the proper channels and they will be stored in the
database.

Here's the [Pull Request](https://github.com/yetibot/yetibot.core/pull/61) that
made these changes.
