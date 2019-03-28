{:title "Yetibot Workshop @ eBay San Jose"
 :layout :post
 :tags  ["presentation" "events" "screencast"]}


![Yetibot Workshop](/img/yetibot_workshop.jpg)

As part of eBay's internal Front End conference,
[@devth](https://github.com/devth) gave a "Contributing to Yetibot" workshop
covering:

- A demo of some of Yetibot's fun and useful features
- Brief history of the project
- Fundamentals of Yetibot usage:
  - Aliases
  - Expression composition via pipes
  - Values and Lists
  - Xargs
  - Data + render
- Livecoding a new feature, adding `forecast` support to the existing weather
  command ([resulting PR!](https://github.com/yetibot/yetibot/pull/901)) with
  the goal of showing off the amazing power of the Clojure language and the
  interactive development workflow

The audience consisted of FE engineers who had zero Clojure experience. During
the livecoding session we went over some Clojure language basics.

To explain fundamentals, we deconstructed the `alltemps` alias, breaking it down
to its individual pieces and testing each command in isolation.

<div class="video-responsive">
<iframe
  width="854" height="480"
  src="https://www.youtube.com/embed/tcFvu6CL2fg?rel=0"
  frameborder="0"
  allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen>
</iframe>
</div>

This was a fun exercise, but to make it even more clear we're planning to build
a front end component that, given an expression, visually breaks down the
expression into its parts, showing the result of each command in the pipeline
and the corresponding data behind them (follow along on
[#900](https://github.com/yetibot/yetibot.github.io/issues/6)).
