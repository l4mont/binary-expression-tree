"""Demonstrate valid expressions and continue after input errors."""
from binary_expression_tree import BinaryExpressionTree


def main():
    for expression in ("5 3 8 * +", "8 2 / 3 -", "1 +", "4 0 /", "-2.5 4 *"):
        print(f"Input: {expression}")
        try:
            tree = BinaryExpressionTree(expression)
            print("Infix:", tree.to_infix())
            print("Postfix:", tree.to_postfix())
            print("Result:", tree.evaluate())
        except (ValueError, ZeroDivisionError) as error:
            print("Error:", error)
        print()


if __name__ == "__main__":
    main()
