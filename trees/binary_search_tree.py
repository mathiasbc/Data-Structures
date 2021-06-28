from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass(order=False)
class BSTNode:
    """
    binary search tree node
    """

    value: Optional[int] = None
    right: Optional["BSTNode"] = None
    left: Optional["BSTNode"] = None

    def insert(self, new_val: int) -> None:
        if new_val > self.value:
            if not self.right:
                self.right = BSTNode(new_val)
            else:
                self.right.insert(new_val)
        else:
            if not self.left:
                self.left = BSTNode(new_val)
            else:
                self.left.insert(new_val)

    def in_order(self, node: "BSTNode") -> Iterable["BSTNode"]:
        """
        Lazy Iterator, aka Generator
        """
        if not node:
            raise StopIteration
        if node.left:
            for _node in self.in_order(node.left):
                yield _node
        yield node
        if node.right:
            for _node in self.in_order(node.right):
                yield _node

    def pre_order(self, node: "BSTNode") -> Iterable["BSTNode"]:
        """
        Can be implemented iteratively using a stack, just like DFS.
        """
        if not node:
            raise StopIteration
        yield node
        if node.left:
            for _node in self.pre_order(node.left):
                yield _node
        if node.right:
            for _node in self.pre_order(node.right):
                yield _node

    def post_order(self, node: "BSTNode") -> Iterable["BSTNode"]:
        if not node:
            raise StopIteration
        if node.left:
            for _node in self.post_order(node.left):
                yield _node
        if node.right:
            for _node in self.post_order(node.right):
                yield _node
        yield node

    def bfs(self, node: "BSTNode") -> Iterable["BSTNode"]:
        """
        Breadth-first search; uses a Queue
        """
        queue = [node]

        while queue:
            current = queue.pop()
            yield current
            if current.left:
                queue.insert(0, current.left)
            if current.right:
                queue.insert(0, current.right)

    def dfs(self, node: "BSTNode") -> Iterable["BSTNode"]:
        """
        Depth-first search; uses a Stack
        """
        stack = [node]

        while stack:
            current = stack.pop()
            yield current
            # Since this is a stack, insert the right
            # first so it gets processed after left
            if current.right:
                stack.append(current.right)
            if current.left:
                stack.append(current.left)

    def serialize(node: "BSTNode") -> str:
        """
        use pre-order traversal to serialize
        """
        return ",".join([str(n.value) for n in node.pre_order(node)])

    @classmethod
    def deserialize(cls, serialized: str) -> "BSTNode":
        """
        Ingest a pre-order serialized tree and insert 
        into new BSTNode class instance.
        """
        node_values = [int(i) for i in serialized.split(",")]
        tree = cls(node_values[0])

        for i in node_values[1:]:
            tree.insert(i)

        return tree

    def right_view(self, node: Optional["BSTNode"]) -> Iterable["BSTNode"]:
        if node:
            yield node
            for _node in self.right_view(node.right):
                yield _node


def check(tree):
    print("In-order")
    for node in tree.in_order(tree):
        print(node.value, end=" ")
    print()

    print("Pre-order")
    for node in tree.pre_order(tree):
        print(node.value, end=" ")
    print()

    print("Post-order")
    for node in tree.post_order(tree):
        print(node.value, end=" ")
    print()

    print("BFS")
    for node in tree.bfs(tree):
        print(node.value, end=" ")
    print()

    print("DFS")
    for node in tree.dfs(tree):
        print(node.value, end=" ")
    print()


def test_is_bst(tree: BSTNode) -> None:
    """
    check if a graph is a BST. This means in-order
    traversal returns ordered elements.
    """
    output = [n.value for n in tree.in_order(tree)]
    assert output == sorted(output)


def test_sum_nodes(tree: BSTNode) -> None:
    print(sum([n.value for n in tree.in_order(tree)]))


def test_serialize_deserialize(tree: BSTNode) -> None:
    serialized = BSTNode.serialize(tree)
    assert serialized == "6,4,3,5,8,7,9"
    assert BSTNode.deserialize(serialized) == tree


def test_right_view(tree: BSTNode) -> None:
    for node in tree.right_view(tree):
        print(node.value)


def test_is_subtree(tree: BSTNode) -> None:
    subtree = BSTNode(4)
    subtree.insert(3)
    subtree.insert(5)

    for _subtree in tree.pre_order(tree):
        if subtree == _subtree:
            print(subtree)
            print(_subtree)
            return True


def leaves_same_level() -> bool:
    # create a tree
    tree = BSTNode(6)
    for i in [4, 8, 3, 5]:
        tree.insert(i)

    stack = [tree]
    leaf_levels = []

    # Awesome python is awesome
    tree.level = 0

    while stack:
        current = stack.pop()
        
        # means is a leaf
        if not current.right and not current.left:
            leaf_levels.append(current.level)

        if current.right:
            current.right.level = current.level + 1
            stack.append(current.right)
        if current.left:
            current.left.level = current.level + 1
            stack.append(current.left)

    print(leaf_levels)
    return len(set(leaf_levels)) == 1


def leave_same_level_recursive(tree, level=0, leaf_levels=None) -> List[Optional[int]]:
    if not leaf_levels:
        leaf_levels = []

    if not tree:
        return [level - 1]
    
    # This is a leaf, return level
    if not tree.right and not tree.left:
        return [level]
    
    leaf_levels.extend(leave_same_level_recursive(tree.left, level + 1, leaf_levels[:]))
    leaf_levels.extend(leave_same_level_recursive(tree.right, level + 1, leaf_levels[:]))

    return leaf_levels


def build_tree_from_ordered(input, tree=None):
    """
    from an ordered List of node values, return a balanced BST
    """

    if len(input) == 0:
        return tree
    if len(input) == 1:
        tree = BSTNode(input[0])
        return tree

    middle_pos = int(len(input) / 2)
    right_tree = input[:middle_pos - 1]
    left_tree = input[middle_pos + 1:]
    actual_node = input[middle_pos - 1:middle_pos][0]

    # insert tree node
    if tree is None:
        tree = BSTNode(actual_node)
    else:
        tree.value = actual_node
    tree.right = build_tree_from_ordered(right_tree, tree=tree.right)
    tree.left = build_tree_from_ordered(left_tree, tree=tree.left)

    return tree


if __name__ == "__main__":
    tree = BSTNode(6)
    for i in [4, 8, 3, 5, 7, 9]:
        tree.insert(i)

    check(tree)
    test_is_bst(tree)
    test_sum_nodes(tree)
    test_serialize_deserialize(tree)
    test_right_view(tree)
    test_is_subtree(tree)

    print(leaves_same_level())
    print(leave_same_level_recursive(tree))
    print(build_tree_from_ordered([3,4,5,6,7,8,9]))
