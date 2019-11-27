from typing import TypeVar, List

T = TypeVar("T")


class Node:
    def __init__(self: T, neighbours: List[T]):
        self.neighbours = neighbours

    def get_neighbours(self) -> List[T]:
        return self.neighbours


class ChildNode(Node):
    def child_method(self):
        pass


child_node = ChildNode([])

for node in child_node.neighbours:
    node.child_method()
