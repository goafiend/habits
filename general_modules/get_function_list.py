import ast
import sys

def get_function_names(file_path):
    """
    Scan a Python file and return a list of all function names.

    :param file_path: Path to the Python file to scan
    :return: List of function names found in the file
    """
    with open(file_path, 'r') as file:
        content = file.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error in file {file_path}: {e}")
        return []

    function_names = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_names.append(node.name)
        elif isinstance(node, ast.ClassDef):
            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef):
                    function_names.append(f"{node.name}.{subnode.name}")

    return function_names

def main():
    if len(sys.argv) < 2:
        print("Usage: python function_scanner.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    functions = get_function_names(file_path)

    if functions:
        print(f"Functions found in {file_path}:")
        for func in functions:
            print(f"- {func}")
        compact = []
        for func in functions:
            compact.append(func)
        with open("output.txt", 'size') as file:
            file.write(f"Functions found:\n")
            file.write(f"{compact}")
        print(compact)

    else:
        print(f"No functions found in {file_path}")

if __name__ == "__main__":
    main()