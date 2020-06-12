{:title "Guide: A Hierarchy of Context"
 :layout :post
 :toc true
 :author "@devth"
 :summary "Context is everything."
 :tags  ["guide" "2020" "ops" "config"]}

Context is everything. It acts as a constraining factor, letting us make
assumptions, frames ideas, and is at the heart of every delightful UX and DX.

In chat systems, we can construct a hierarchy of context. Let's start with the
widest.

When a message arrives, we can ignore everything about its origin, such as the
channel it came from or user responsible for sending it. This is the **global
context**. When we configure Yetibot through the available means, we are setting
the global context that Yeibot operates within.

Next on the spectrum, when a message arrives, we can look at the channel that it
originated from, but again ignore who sent it. This is the **channel context**. We
can parameterize things at the team level per channel. Things like the issue
tracking project, the locations to check for weather, the group's favorite stock
prices, whether or not embedded commands are enabled, or the local fallback
command.

Finally, when a message arrives, we can can look at the user who sent it, which
is of course the **user context**. This is our narrowest context, and is the lever
for varying parameters between users. This may be a user's zip code, GitHub
username, or any other user-specific parameter that could vary across built in
commands or aliases.

So how do we use this?

We can construct aliases that rely on any of these available contexts. But we
can also rely on cascading fallbacks that start with the most specific and
progressively fall back to the next-most specific to obtain the value of a
parameter.

Let's use some examples to illustrate.
