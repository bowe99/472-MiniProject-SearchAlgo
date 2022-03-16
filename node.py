from enum import Enum

class Node:
    def __init__(self, parent, depth, state) -> None:
        self.parent = parent
        self.depth = depth
        self.state = state

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.state == other.state
        return False

class Move(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4