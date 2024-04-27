## Tree Printer

- single file import / copy for generic tree console printing
- based off https://github.com/AharonSambol/PrettyPrintTree
    - extracted only vertical printing
    - removed color based printing
- standard library only, no dependencies apart from appropriate python version required `>=3.7`

## Usage

This is a skeleton example. Please refer to `example.py` for a runnable example.

```python
from treeprinter import printree

@dataclass
class Node:
    val: int = 0
    left: Optional[Node] = None
    right: Optional[Node] = None

root = ... # some tree init based on Node

printree(
    node=root,
    get_children=lambda n: [x for x in [n.left, n.right] if x is not None],
    get_value=lambda n: n.val,
)
```