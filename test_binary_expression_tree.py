import unittest
from binary_expression_tree import BinaryExpressionTree


class ExpressionTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(BinaryExpressionTree("2 3 +").evaluate(), 5)

    def test_nested(self):
        tree = BinaryExpressionTree("5 3 8 * +")
        self.assertEqual(tree.to_infix(), "(5 + (3 * 8))")
        self.assertEqual(tree.to_postfix(), "5 3 8 * +")
        self.assertEqual(tree.evaluate(), 29)

    def test_order(self):
        self.assertEqual(BinaryExpressionTree("8 2 / 3 -").evaluate(), 1)

    def test_negative_decimal(self):
        self.assertAlmostEqual(BinaryExpressionTree("-1.2 0.5 *").evaluate(), -0.6)

    def test_malformed(self):
        for expression in ("", "1 +", "1 2", "1 x +"):
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                BinaryExpressionTree(expression)

    def test_zero_division(self):
        tree = BinaryExpressionTree("4 0 /")
        with self.assertRaises(ZeroDivisionError):
            tree.evaluate()

    def test_positions_and_traversals(self):
        tree = BinaryExpressionTree("8 2 / 3 -")
        root = tree.root()
        left = tree.left(root)
        self.assertEqual(left.element(), "/")
        self.assertEqual(tree.parent(left), root)
        self.assertEqual(tree.right(root).element(), "3")
        self.assertIsNone(tree.parent(root))
        self.assertIsNone(tree.left(tree.right(root)))
        self.assertEqual([p.element() for p in tree.preorder()], "- / 8 2 3".split())
        self.assertEqual([p.element() for p in tree.inorder()], "8 / 2 - 3".split())
        self.assertEqual([p.element() for p in tree.postorder()], "8 2 / 3 -".split())


if __name__ == "__main__":
    unittest.main()
