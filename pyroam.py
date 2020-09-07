"""
PyRoam

Simple python interface for Roam Research graphs.

NOTES:
- title is the uid for notes

TODO:
x parse [[bracket references]] and #tags and ((block refs))

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
    children: List["Block"]  # Forward reference a la PEP 484
    uid: str

    # TODO: make these datetimes
    edit_time: str
    edit_email: str
    create_time: str
    create_email: str

    # found on children only
    string: str
    heading: str  # NOTE: not sure what this is

    def __post_init__(self):
        self.child_blocks = [get_block(b) for b in self.children or []]
        self.type = "NOTE" if self.uid is None else "BLOCK"

        # sanity checks
        if self.title and self.string:
            raise Exception("title and string expected mutually exclusive")

    def text(self):
        return self.title or self.string

    def id(self):
        return self.title or self.uid

    def id_references(self):

        return sorted(
            set(
                match
                for regex in [TAG_REGEX, BRACKETS_REGEX, PARENS_REGEX]
                for match in re.findall(regex, self.text())
            )
        )

    def references(self, graph):
        """
        Assumes graph is a list of all blocks in all pages.
        """
        return [next(b for b in graph if b.id() == ref) for ref in self.id_references()]

    def child_id_references(self):
        return sorted(
            set(match for child in self.child_blocks for match in child.id_references())
        )

    def descendant_blocks(self):
        return self.child_blocks + [
            cb for child in self.child_blocks for cb in child.child_blocks
        ]

    def descendant_id_references(self):
        return sorted(
            set(ref for b in self.descendant_blocks() for ref in b.id_references())
        )


def read(filepath):
    user_fp = os.path.expanduser(filepath)
    with open(user_fp) as f:
        return json.load(f)


@dataclass
class Graph:

    blocks: List[Block]

    def all_blocks(self):
        return self.blocks + [db for b in self.blocks for db in b.descendant_blocks()]


def get_block(b: dict):
    return Block(
        title=b.get("title"),
        uid=b.get("uid"),
        children=b.get("children"),
        string=b.get("string"),

        edit_time=b.get("edit-time"),
        edit_email=b.get("edit-email"),
        create_time=b.get("create-time"),
        create_email=b.get("create-email"),
        heading=b.get("heading"),
    )


def blocks():
    contents = read(FILEPATH)
    return [get_block(b) for b in contents]


def main():
    all_blocks = blocks()
    g = Graph(all_blocks)


if __name__ == "__main__":
    main()
