{:title "Guide: A Hierarchy of Context"
 :layout :post
 :toc true
 :author "@devth"
 :summary "Mine, ours, theirs"
 :tags  ["guide" "2020" "ops" "config"]}

```yetibot
!complete context is
```

Context is everything. It acts as a constraining factor, letting us make
assumptions, frames ideas, and is at the heart of every delightful UX and DX.

In chat systems, we can construct a hierarchy of context. Let's start with the
widest.

## Global

When a message arrives, we can ignore everything about its origin, such as the
channel it came from or user responsible for sending it. This is the
**global context**. It spans an entire Yetibot instance across all configured
adapters.

## Adapter

Slightly more specific, when a message arrives we can look at the adapter that
it originated from. This is the **adapter context**.

## Channel

Next on the spectrum, when a message arrives, we can look at the channel that it
originated from, but again ignore who sent it. This is the **channel context**. We
can parameterize things at the team level per channel. Things like the issue
tracking project, the locations to check for weather, the group's favorite stock
prices, whether or not embedded commands are enabled, or the local fallback
command.

## User

Finally, when a message arrives, we can can look at the user who sent it, which
is of course the **user context**. This is our narrowest context, and is the lever
for varying parameters between users. This may be a user's zip code, GitHub
username, or any other user-specific parameter that could vary across built in
commands or aliases.

## Usage and examples

So how do we use this?

We can construct aliases that rely on any of these available contexts. But we
can also rely on cascading fallbacks that start with the most specific and
progressively fall back to the next-most specific to obtain the value of a
parameter.

Let's use some examples to illustrate.

### Weather

**Use case**: quickly list the current weather for all members in the channel.

There are a couple ways to do this. But first, let's define a helper alias:

```yetibot
!alias loctemp = "weather $s | render {{temp|multiply:1.8|add:32|round}}°F, Humidity {{rh}}% - {{weather.description}}, {{city_name}}, {{state_code}} {{country_code}}"
```

#### Channel settings

Now, let's say you have people in the channel from Seattle, Chicago, and New
York City. We can encode that in a channel setting:

```yetibot
!channel set locs = Seattle, Chicago, New York City
```

```yetibot
!alias chantemps = "channel settings locs | list | xargs loctemp | sort"
```

Finally, try it out:

```yetibot
!chantemps
```

This allows us to vary the set of `locs` from channel to channel.
The result of `chantemps` will reflect the local channel settings.

#### User settings

Another way to solve this weather look up use case would be for individuals to
set their individual locations via `my`.

```yetibot
!help my
```

This is interesting, because once a user sets their location, a command that
utilizes the locations of all members in a channel would vary from channel to
channel automatically, depending on who is present. When a user leaves or joins
a channel, the context is updated accordingly.

We can get that list of values using `our`:

```yetibot
!help our
```

```yetibot
!our zip
```

### Stocks

Use case: list stock prices.

This time let's rely on `ours`.

```yetibot
!my stocks = aapl,goog,tsla
```

Now if another user specified:

```yetibot
```

## Future

In the future, as part of
[The great configuration overhaul of 2020](https://github.com/yetibot/yetibot/projects/5),
we may provide the ability to override immutable Yetibot configuration at
runtime with mutable (i.e. stored in the database) config.

