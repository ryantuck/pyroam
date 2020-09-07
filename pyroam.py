"""
PyRoam

Simple python interface for Roam Research graphs.

NOTES:
- i'm calling 'pages' blocks for simplicity's sake, though subclassing would likely be cleaner.
- title is the id for 'pages'
- uid is the id for blocks
- a graph is the single object entrypoint, and blocks are stored in the hierarchy from there.

TODO:
x parse [[bracket references]] and #tags and ((block refs))
x fix the goddamn block repr
- cli interface with queries, filters, etc.
- get typing right
- more meaningful diffs between pages and blocks
- add tests!
    - regex
    - sample graph
- add support for unlinked references
- add support for networkx representation
- more fully-featured search

"""
from dataclasses import dataclass
from typing import List
import json
import os
import re

FILEPATH = "~/Downloads/ryantuck.json"

TAG_REGEX = r"#([A-Za-z0-9-]*)"  # NOTE: doesn't support tags with spaces
BRACKETS_REGEX = r"\[\[([A-Za-z0-9- ]*)\]\]"
PARENS_REGEX = r"\(\(([A-Za-z0-9- ]*)\)\)"


@dataclass
class Block:

    title: str
    children: List["Block"]  # 'Forward reference' support for recursion a la PEP 484
    uid: str
    string: str

    # TODO: make these datetimes
    _edit_time: str
    _edit_email: str
    _create_time: str
    _create_email: str
    _heading: str  # NOTE: not sure what this is

    def __post_init__(self):
        self.type = "NOTE" if self.uid is None else "BLOCK"

        # sanity checks
        if self.title and self.string:
            raise Exception("title and string expected mutually exclusive")
        if self.title and self.uid:
            raise Exception("title and uid expected mutually exclusive")

    def __repr__(self):
        return f'{self.type} | {self.id()} | c{len(self.children)}d{len(self.descendants())} | {self.text()}'

    def text(self):
        return self.title or self.string

    def id(self):
        return self.title or self.uid

    def _id_references(self):

        return sorted(
            set(
                match
                for regex in [TAG_REGEX, BRACKETS_REGEX, PARENS_REGEX]
                for match in re.findall(regex, self.text())
            )
        )

    def _child_id_references(self):
        return sorted(
            set(match for child in self.children for match in child._id_references())
        )

    def _descendant_id_references(self):
        return sorted(
            set(ref for b in self.descendants() for ref in b._id_references())
        )

    def references(self, graph):
        """
        Assumes graph is a list of all blocks in all pages.
        """
        return [
            next(b for b in graph if b.id() == ref) for ref in self._id_references()
        ]

    def linked_references(self, graph):
        """
        Return all blocks that reference this block.
        """
        return [b for b in graph.all_blocks() if self.id() in b.references()]

    def descendants(self):
        return self.children + [cb for child in self.children for cb in child.children]


@dataclass
class Graph:

    filepath: str

    def __post_init__(self):
        self._data = read_graph_json_file(self.filepath)
        self.blocks = [get_block(b) for b in self._data]
        print(len(self.blocks))

    def all_blocks(self):
        return self.blocks + [db for b in self.blocks for db in b.descendants()]

    def get_block(self, block_id):
        """
        Returns Block with given `block_id`.
        """
        return next(b for b in self.all_blocks() if b.id() == block_id)

    def search(self, query):
        """
        Rudimentary search for blocks containing `query` in their `text` or `id`.
        """
        return [b for b in self.all_blocks() if query in b.text() or query in b.id()]


def read_graph_json_file(filepath):
    user_fp = os.path.expanduser(filepath)
    with open(user_fp) as f:
        return json.load(f)


def get_block(b: dict):
    """
    Return a Block object from its JSON representation.
    """
    return Block(
        title=b.get("title"),
        uid=b.get("uid"),
        children=[get_block(c) for c in b.get("children", [])],
        string=b.get("string"),
        _edit_time=b.get("edit-time"),
        _edit_email=b.get("edit-email"),
        _create_time=b.get("create-time"),
        _create_email=b.get("create-email"),
        _heading=b.get("heading"),
    )


def get_graph(filepath):
    return Graph(filepath)


def main():
    g = get_graph(FILEPATH)


if __name__ == "__main__":
    main()
