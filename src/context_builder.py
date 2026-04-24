import ast

def extract_function_code(file_path, function_names):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    functions = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in function_names:
            functions[node.name] = ast.get_source_segment(open(file_path).read(), node)

    return functions


def extract_imports(file_path):
    imports = []
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.get_source_segment(open(file_path).read(), node))

    return "\n".join(imports)