{:title "All your data are belong"
 :layout :post
 :tags  ["core" "2019" "data"]}

In the last few months we've been working on including raw data in command
responses.

- clj can now access that data thanks to an awesome idea by one of our newest
  contributors, [@justone](https://github.com/justone).
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
