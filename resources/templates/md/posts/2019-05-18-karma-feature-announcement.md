{:title "Karma Feature Announcement"
 :layout :post
 :author "@jcorrado"
 :summary "The Yetibot Team just recently added a new feature called Karma."
 :image "/img/screenshots/karma_user_score.png"
 :tags  ["core" "news" "2019"]}

The Yetibot Team just recently added a new feature called Karma.  It's an implementation of the classic IRC feature of the same name, with a few updates, and support for Slack interface opportunities.

One of the summary notions we kick around in the project is "Community Command Line".  To me, this is all about building an interface to our work that lets more people participate in decisions and review their outcomes.  It's a big goal, and it's all about community.

Part of any community is recognition.  It's how we show our appreciation when someone helps us, and how we identify our experts so others, with new problems to tackle, know where to start looking for help.  With Yetibot's focus on communalizing work, adding a feature to give thanks and communicate accomplishments felt like a natural fit.

The idea is simple: you give a point to someone, and optionally supply a note, when you want to recognize them.  It's quick and easy.

The `!karma` command is the canonical interface, and it uses the C increment operator, `++`, as has typically been the custom in classic IRC implementations.  We like traditions so we stuck with that as the basic operation.

![karma basic interface](/img/screenshots/karma_basic_iface.png)

But you can also use Slack's [Emoji Reactions](https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions) to quickly cheer something; a quick nod of thanks.

![karma emoji reaction interface](/img/screenshots/karma_emoji_reaction_iface.png)

You can't supply a comment in this case, and Yetibots score update for the recipient is communicated in a thread to keep your channel uncluttered.

A third interface, somewhere in between the two, is to use the trigger emojis as a verb.

![karma emoji verb interface](/img/screenshots/karma_emoji_verb_iface.png)

You can see a compact leader board

![karma leaderboard](/img/screenshots/karma_leaderboard.png)

Or a particular user's score and recent comments, too.

![karma user score](/img/screenshots/karma_user_score.png)

For next steps, we'd like to start making use of the [digraph](https://en.wikipedia.org/wiki/Directed_graph) created as people show their appreciation for one another.  There's a commutative "web" of appreciation we form as we interact.  It might be fun to see how communities enmesh as members support each other.  How many degrees of separation are there in your community?  Yetibot might be able to help answer that someday.

For now, we hope you enjoy the simple act of giving and getting thanks.  Have a look through the [User Guide](https://yetibot.com/user-guide#karma) for more details on the interface, including our first steps on publishing reports via the GraphQL API
