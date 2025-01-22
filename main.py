import re
from prettytable import PrettyTable
import sympy as sp

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def build_parallel_tree(expression):
    expression = expression.replace(" ", "")
    operands = [Node(ch) for ch in re.findall(r'\w+|\d+\.?\d*', expression)]
    operators = [Node(ch) for ch in expression if ch in "+-*/"]

    if len(operands) - 1 != len(operators):
        raise ValueError("Invalid expression: mismatch between operands and operators.")

    while len(operands) > 1:
        new_level = []
        for i in range(0, len(operands) - 1, 2):
            operator = operators.pop(0)
            operator.left = operands[i]
            operator.right = operands[i + 1]
            new_level.append(operator)
        if len(operands) % 2 == 1:
            new_level.append(operands[-1])
        operands = new_level

    return operands[0]

def collect_levels(root):
    if not root:
        return []

    levels = []

    def traverse(node, depth):
        if len(levels) <= depth:
            levels.append([])
        levels[depth].append(node)
        if node:
            traverse(node.left, depth + 1)
            traverse(node.right, depth + 1)

    traverse(root, 0)
    return levels

def print_parallel_tree_with_table(root):
    if not root:
        print("Empty tree")
        return

    levels = collect_levels(root)
    max_width = 2 ** (len(levels) - 1)

    rows = []
    for depth, level in enumerate(levels):
        row = [" "] * max_width
        spacing = max_width // (2 ** depth)
        for i, node in enumerate(level):
            if node:
                position = i * spacing + spacing // 2
                row[position] = node.data
        rows.append(row)

    for row in rows:
        print("".join(f"{item:^3}" for item in row))

def evaluate_expression(expression):
    try:
        # Use sympy to simplify the expression
        simplified_expr = sp.simplify(sp.sympify(expression))
        return simplified_expr
    except Exception as e:
        return str(e)

def main():
    while True:
        expression = input("Enter an arithmetic expression (or 'exit' to quit): ")
        if expression.lower() == 'exit':
            break
        try:
            root = build_parallel_tree(expression)
            print("Parallel tree:")
            print_parallel_tree_with_table(root)
            result = evaluate_expression(expression)
            print(f"Result: {result}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
