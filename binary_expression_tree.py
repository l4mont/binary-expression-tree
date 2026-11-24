"""Linked, positional expression tree built from postfix tokens."""
from stack import Stack


class _Node:
    __slots__ = ("token", "parent", "left", "right")

    def __init__(self, token, left=None, right=None):
        self.token = token
        self.parent = None
        self.left = left
        self.right = right
        if left is not None:
            left.parent = self
            right.parent = self


class Position:
    def __init__(self, tree, node):
        self._tree = tree
        self._node = node

    def element(self):
        return self._node.token

    def __eq__(self, other):
        return isinstance(other, Position) and self._tree is other._tree and self._node is other._node


class BinaryExpressionTree:
    """Accept numbers and +, -, *, /. Malformed postfix raises ValueError."""

    def __init__(self, postfix):
        trees = Stack()
        for token in postfix.split():
            if token in ("+", "-", "*", "/"):
                if trees.size() < 2:
                    raise ValueError(f"Too few operands for {token}")
                right = trees.pop()
                left = trees.pop()
                # Only stack entries own partial roots. Popping transfers both
                # roots into the new subtree without copying any descendants.
                trees.push(_Node(token, left, right))
            else:
                try:
                    float(token)
                except ValueError as error:
                    raise ValueError(f"Unsupported token: {token}") from error
                trees.push(_Node(token))
        if trees.is_empty():
            raise ValueError("Empty expression")
        if trees.size() != 1:
            raise ValueError("Extra operands")
        self._root = trees.pop()

    def root(self):
        return Position(self, self._root)

    def _relative(self, p, attribute):
        if not isinstance(p, Position) or p._tree is not self:
            raise ValueError("Position belongs to another tree")
        node = getattr(p._node, attribute)
        return Position(self, node) if node is not None else None

    def left(self, p):
        return self._relative(p, "left")

    def right(self, p):
        return self._relative(p, "right")

    def parent(self, p):
        return self._relative(p, "parent")

    def _walk(self, node, order):
        if node is None:
            return
        if order == "pre":
            yield Position(self, node)
        yield from self._walk(node.left, order)
        if order == "in":
            yield Position(self, node)
        yield from self._walk(node.right, order)
        if order == "post":
            yield Position(self, node)

    def preorder(self):
        return self._walk(self._root, "pre")

    def inorder(self):
        """Raw inorder traversal emits tokens without parentheses."""
        return self._walk(self._root, "in")

    def postorder(self):
        return self._walk(self._root, "post")

    def to_postfix(self):
        return " ".join(p.element() for p in self.postorder())

    def to_infix(self):
        parts = []

        def visit(node):
            if node.left is None:
                parts.append(node.token)
                return
            parts.append("(")
            visit(node.left)
            parts.extend((" ", node.token, " "))
            visit(node.right)
            parts.append(")")

        visit(self._root)
        return "".join(parts)

    def evaluate(self):
        """Evaluate recursively. Division by zero raises ZeroDivisionError."""
        def value(node):
            if node.left is None:
                return float(node.token)
            left = value(node.left)
            right = value(node.right)
            if node.token == "+":
                return left + right
            if node.token == "-":
                return left - right
            if node.token == "*":
                return left * right
            return left / right

        return value(self._root)
