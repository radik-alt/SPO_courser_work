from typing import List


class Node:

    def __init__(self):
        self.name = None,
        self.type = 0,
        self.parent = Node or None,
        self.children = List[Node]
        self.branch = [],
        self.currentBranch: str = ""
        self.checkout: bool = False


    def __str__(self):
        return self.name
