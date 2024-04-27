"""Tree Console Printing Utility"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, TypeVar

__NodeType = TypeVar("__NodeType")
__T = TypeVar("__T")


@dataclass
class __StyleNode:
    lines: list[str]
    height: int
    width: int
    middle_width: int = None

    @classmethod
    def from_str(cls, content: str) -> __StyleNode:
        lines = content.split("\n")
        height = len(lines)
        width = max(len(line) for line in lines)
        return cls(lines, height, width)

    def get_middle_width(self) -> int:
        if self.middle_width is None:
            return sum(divmod(self.width, 2)) - 1
        return self.middle_width

    def to_str(self) -> str:
        return "\n".join(self.lines)


def __ljust(text: str, amount: int, padding: str = " ") -> str:
    return text + padding * (amount - len(text))


def __zip_longest(*iters: list[__T], default: __T):
    lens = [len(x) for x in iters]
    for line in range(max(lens)):
        yield tuple(
            itr[line] if line < lens[i] else default for i, itr in enumerate(iters)
        )


def __join_boxes(boxes: list[__StyleNode]) -> tuple[list[str], int, int]:
    lines = [
        " ".join(__ljust(line, boxes[i].width) for i, line in enumerate(lines))
        for lines in __zip_longest(*(box.lines for box in boxes), default="")
    ]
    width = sum(box.width for box in boxes) + len(boxes) - 1
    height = max(box.height for box in boxes)
    return lines, width, height


def __add_pipes(boxes: list[__StyleNode], lines: list[str]) -> int:
    padding = " " * boxes[0].get_middle_width()
    pipes = "┌"
    for prev, box in zip(boxes, boxes[1:]):
        pipes += (
            "─" * (prev.width - prev.get_middle_width() + box.get_middle_width()) + "┬"
        )
    middle_of_pipes = sum(divmod(len(pipes), 2)) - 1
    pipes = (
        padding
        + pipes[:middle_of_pipes]
        + {"─": "┴", "┬": "┼", "┌": "├", "┐": "┤"}[pipes[middle_of_pipes]]
        + pipes[middle_of_pipes + 1 : -1]
        + "┐"
    )
    lines.insert(0, pipes)
    return len(padding) + middle_of_pipes


def __join_horizontal(boxes: list[__StyleNode]) -> __StyleNode:
    lines, width, height = __join_boxes(boxes)
    middle_width = __add_pipes(boxes, lines)
    height += 1
    return __StyleNode(lines, height, width, middle_width)


def __add_parent_top(parent: __StyleNode, children: __StyleNode) -> __StyleNode:
    parent_middle_width, children_middle_width = (
        parent.get_middle_width(),
        children.get_middle_width(),
    )
    parent_width, children_width = parent.width, children.width
    if parent_middle_width == children_middle_width:
        lines = parent.lines + children.lines
        middle_width = parent_middle_width
    elif parent_middle_width < children_middle_width:
        padding = " " * (children_middle_width - parent_middle_width)
        lines = [padding + line for line in parent.lines] + children.lines
        parent_width += children_middle_width - parent_middle_width
        middle_width = children_middle_width
    else:
        padding = " " * (parent_middle_width - children_middle_width)
        lines = parent.lines + [padding + line for line in children.lines]
        children_width += parent_middle_width - children_middle_width
        middle_width = parent_middle_width
    return __StyleNode(
        lines,
        height=parent.height + children.height,
        width=max(parent_width, children_width),
        middle_width=middle_width,
    )


def __vertical_join(
    node: __NodeType,
    get_children: Callable[[__NodeType], Iterable[__NodeType]],
    get_value: Callable[[__NodeType], Any],
    depth: int = 0,
    max_depth: int = -1,
) -> __StyleNode:
    children = get_children(node)
    sn = __StyleNode.from_str(str(get_value(node)))
    if children and (max_depth == -1 or depth < max_depth):
        style_children_nodes = [
            __vertical_join(c, get_children, get_value, depth + 1, max_depth)
            for c in children
        ]
        if len(children) == 1:
            scn = style_children_nodes[0]
            scn.lines.insert(0, " " * scn.get_middle_width() + "|")
        else:
            scn = __join_horizontal(style_children_nodes)
        sn = __add_parent_top(sn, scn)
    return sn


def printree(
    node: __NodeType,
    get_children: Callable[[__NodeType], Iterable[__NodeType]],
    get_value: Callable[[__NodeType], Any],
    *,
    max_depth: int = -1,
    return_as_str: bool = False,
) -> str | None:
    """
    Prints tree to console based on general node type.

    Examples:

    # n-ary tree
    printree(
        node=node,
        get_children=lambda x: x.children,
        get_value=lambda x: x.val
    )

    # binary tree
    printree(
        node=node,
        get_children=lambda n: [x for x in [n.left,  n.right] if x is not None],
        get_value=lambda x: x.val
    )

    :param node: general node object, must have children and value
    :type node: NodeType
    :param get_children: method to retrieve children of node, should be same type as parent node
    :type get_children: Callable[[NodeType], Iterable[NodeType]]
    :param get_value: method to retrive value of node
    :type get_value: Callable[[NodeType], Any]
    :param max_depth: maximum printable tree depth, no limits if -1 (default is -1)
    :type max_depth: int, optional
    :param return_as_str: returns output as string, otherwise prints to stdout, defaults to False
    :type return_as_str: bool, optional
    :return: returns formatted output as string or prints to stdout depending on "return_as_str" variable
    :rtype: str | None
    """
    output = __vertical_join(
        node, get_children, get_value, max_depth=max_depth
    ).to_str()

    if not return_as_str:
        print(output)
        return

    return output
