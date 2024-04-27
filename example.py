from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from treeprinter import printree


@dataclass
class Node:
    val: int = 0
    left: Optional[Node] = None
    right: Optional[Node] = None


def build_tree(values: list[int]) -> Node:
    if not values:
        return None
    vvalues = deepcopy(values)
    root = Node(vvalues.pop(0))
    q = [root]
    while q:
        for _ in range(len(q)):
            node = q.pop(0)
            if node and vvalues:
                node.left = Node(vvalues.pop(0))
                node.right = Node(vvalues.pop(0))
                q.append(node.left)
                q.append(node.right)
    q = [root]
    while q:
        curr: Node = q.pop(0)
        if curr.left:
            if curr.left.val is None:
                curr.left = None
            else:
                q.append(curr.left)
        if curr.right:
            if curr.right.val is None:
                curr.right = None
            else:
                q.append(curr.right)
    return root


root = build_tree(
    [
        213,
        14444,
        3222222222,
        234123412341234,
        43434,
        2,
        77,
        3333,
        666,
        87,
        2,
        789,
        33,
        999999999,
        2123,
    ]
)

printree(
    node=root,
    get_children=lambda n: [x for x in [n.left, n.right] if x is not None],
    get_value=lambda n: n.val,
)
