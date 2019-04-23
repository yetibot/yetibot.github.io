{:title "All your data are belong"
 :layout :post
 :tags  ["core" "2019" "data"]}

In the last few months we've been working on including raw data in command
responses in addition to the formatted lossy-but-human-friendly derived value.

This lets us display the formatted values by default without giving up the full
data in the process, and affords the user the option of tapping into these data
using a few special commands that know how to access it.

The primary data-aware commands are:

```yetibot
!help data
```

```yetibot
!help clj
```

```yetibot
!help render
```

as well as most of the collection utilities, which simply propagate the correct
data across the pipe.

```yetibot
!category list collection
```

## clj

Having the data available means we can reference any piece of the shape instead
of the default human-friendly representation. One way to do this is with the
`clj` command, thanks to an awesome idea by one of our newest contributors,
[@justone](https://github.com/justone) to make the data available to `clj` (he
also contributed the `cljquote` command).

```yetibot
!cljquote
```

First, let's use `data` to get at the data itself, then pass that over to `keys`
to see what's available:

```yetibot
!cljquote | data | keys
```

Then, with this information we can extract just the piece we're interested in:


```yetibot
!cljquote | clj (:clojure-quotes.core/text data)
```

`clj` can access the data from the pipe as a special var called `data`.

## data

The data command also provides a way to pretty print all the data or grab a
specific piece using [json-path](https://goessner.net/articles/JsonPath/)
syntax.

```yetibot
!help data
```

```yetibot
!twitter display 1095377246494220288 | data show
```

```yetibot
!twitter display 1095377246494220288 | data | keys
```

These data represent a retweet with comment. Let's use `data` to grab the
full text of the original tweet:

```yetibot
!twitter display 1095377246494220288 | data $.quoted_status.full_text
```

We could do the same with `clj` using pure Clojure functions:

```yetibot
!twitter display 1095377246494220288 | clj (get-in data [:quoted_status :full_text]
```

And if we wanted to render multiple properties of the retweet, we could combine
`data` and `render`:

```yetibot
!twitter display 1095377246494220288 | data $.quoted_status | render {{full_text}} – @{{user.screen_name}} {{created_at}}
```

## Propagation in collections

Collection utilities are data-aware as well, so when you transform a collection
with a utility like `head`, `tail`, `random` or `grep` (among others), the data
are preserved.

```yetibot
!twitter show yetibot_chatops | random | data show
```

```yetibot
!twitter show yetibot_chatops | head 3 | data show
```

This works because there is symmetry between `:result/data` and `:result/value`.
However, this doesn't mean that `:result/data` must be a sequential collection.
Often times API responses return a top level map as the body with useful
attributes like `:total-count` or other meta data, then return the collection as
an attribute of that map, e.g. `:items`. In cases like these we don't want to
give up those potentially-useful attributes, so instead commands can return an
optional KV in their response, e.g.:

```clojure
{:result/value ["red" "green" "blue"]
 :result/data {:total-count 3
               :response-ms 228
               :items [{:display-name "red"
                        :hex "#ff0000"
                        :id 1}
                       {:display-name "green"
                        :hex "#00ff00"
                        :id 2}
                       {:display-name "blue"
                        :hex "#0000ff"
                        :id 3}]}
 :result/collection-path [:items]}
```


  - demo
- a bunch of commands (github, twitter, jira, ...) support data now
  - demo
- collection commands now do the right thing with the data
  - head, tail, grep, droplast, keys, vals, etc
  - demo
- commands can return a top level response with a pointer to the collection part
  of the structure to power collection utils. This powers the "symmetry" aspect
  of `:result/data` and `:result/value`. Internal command pipeline will use this
  to provide a `data-collection` key/value in the cmd arguments map.
- we'll be rapidly increasing `data` coverage of existing commands


## Docs

See the [data docs](https://yetibot.com/user-guide#data) for more details.
