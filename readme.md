# pyroam

Read your [Roam Research](https://roamresearch.com) graph as python objects.

_Note: this is very alpha. Currently, 'pages' are treated as blocks, and there is room for improvement on the querying side of things. That being said, it does the job.

For features and bugs, please raise an issue or open a PR!_

## Usage

Export your graph in JSON format, then read it in:

```python
import pyroam
g = Graph('~/Downloads/graph.json')
```

Search all block titles:

```
>>> g.search('home')

[NOTE | home | c5d56 | home,
 NOTE | homebrew | c0d0 | homebrew,
 BLOCK | YrcTL0k1D | c0d0 | bring home data modeling guidelines draft,
 BLOCK | Wb4e_vZvD | c2d9 | Roam versus homegrown solution for notes. Hard to pick. Homegrown feels right, but intuition isn't the best guide always.,
 BLOCK | g92mLLO7d | c0d0 | {{{[[DONE]]}}}} Check Amazon order for cat food and repurchase #home,
 BLOCK | jWUgTVgaB | c0d0 | {{[[TODO]]}} Hang vacuum cleaner #home,
 BLOCK | v3qcIx9jz | c0d0 | {{[[TODO]]}} Set up Wii #home,
 BLOCK | t9BeiBpol | c0d0 | {{{[[DONE]]}}}} attach rug grips #home,
 BLOCK | F3NFeiJhZ | c0d0 | {{{[[DONE]]}}}} Fix net on porch #home,
 BLOCK | aufa-pryv | c0d0 | {{{[[DONE]]}}}} Bring paintings from pantry downstairs #home #bs,
 ...
```

Get a specific block by id:

```python
home = g.get_block('home')
```

View children and descendants:

```
>>> home.children()

[BLOCK | KzuCRQz6Y | c4d8 | Utilities,
 BLOCK | gwQD5H3wS | c1d1 | Renters insurance,
 BLOCK | ho9a8j6iM | c0d0 | [[tracking]] security deposit,
 BLOCK | CjZKfNHsZ | c1d6 | Inventory,
 BLOCK | o_UvQf672 | c45d64 | todos]

>>> home.children()[0]

BLOCK | KzuCRQz6Y | c4d8 | Utilities

>>> home.children()[0].descendants()

[BLOCK | 8QKbyzad_ | c1d4 | Water,
 BLOCK | rKmaLoEH9 | c1d4 | Gas,
 BLOCK | HA8dlINJp | c1d4 | Electric,
 BLOCK | MmRplogfU | c1d1 | Internet,
 BLOCK | a3j8BlLUq | c3d3 | Metro Water,
 BLOCK | d_LmRLJr- | c3d3 | Piedmont,
 BLOCK | ddWfOiMZT | c3d7 | NES,
 BLOCK | ukjmO0ZHb | c0d0 | Comcast]
```

Get all linked references in descendants of 'home':

```
>>> set([ref.text() for block in home.descendants() for ref in block.references(g)])

{'DONE',
 'Michael',
 'TODO',
 'basement',
 'bb',
 'bs',
 'buy',
 'car',
 'errand',
 'home',
 'office',
 'tracking',
 'yard'}
```

Find all references to 'home' in the rest of the graph:

```
>>> home.linked_references(g)

[BLOCK | EmHfO-cPS | c0d0 | I set up subscribe n save for paper towels #home,
 BLOCK | jU8_D0cFZ | c1d1 | Inventory checklist for #home,
 BLOCK | 8zXDfoqVb | c0d0 | we have four more curtain rods at [[home]],
 BLOCK | wcfoYzsM- | c0d0 | {{{[[DONE]]}}}} #buy doorstop #home,
 BLOCK | p8dYatt6D | c0d0 | [[home]],
 BLOCK | 2eLBmNphV | c0d0 | {{[[TODO]]}} go through papers #home,
 ...
```



## Motivation

I recently went all-in on Roam after putting together a homegrown markdown-based system for personal knowledge management. Previously, I could publish a subset of those markdown notes to http://ryantuck.io/notes/start/, and I wanted similar functionality in for my second mind in Roam. Until they expose an API, I figured exposing a rudimentary python interface ontop of the (very simple) data model could serve as the basis for publishing scripts.

I didn't find any prior art for this, so I spent an afternoon whipping it up!
