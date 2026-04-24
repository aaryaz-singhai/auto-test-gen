import os
from diff_parser import get_git_diff, extract_changed_functions
from context_builder import extract_function_code, extract_imports
from test_generator import generate_tests
from test_runner import run_tests
from feedback_loop import fix_tests

SOURCE_FILE = "sample.py"   # change as needed


def save_test_file(function_name, test_code):
    os.makedirs("tests", exist_ok=True)
    file_path = f"tests/test_{function_name}.py"

    with open(file_path, "w") as f:
        f.write(test_code)

    return file_path


def main():
    print("🔍 Detecting changes...")
    diff = get_git_diff()
    functions = extract_changed_functions(diff)

    if not functions:
        print("No new functions detected.")
        return

    print(f"🧠 Functions found: {functions}")

    imports = extract_imports(SOURCE_FILE)
    function_map = extract_function_code(SOURCE_FILE, functions)

    for fn_name, fn_code in function_map.items():
        print(f"⚙️ Generating tests for {fn_name}...")

        test_code = generate_tests(fn_name, fn_code, imports)
        path = save_test_file(fn_name, test_code)

        print(f"🧪 Running tests for {fn_name}...")
        result = run_tests()

        if not result["passed"]:
            print("❌ Tests failed. Attempting fix...")

            fixed_code = fix_tests(fn_name, fn_code, imports, result["output"])
            save_test_file(fn_name, fixed_code)

            result = run_tests()

            if result["passed"]:
                print("✅ Tests fixed successfully")
            else:
                print("⚠️ Still failing. Manual review needed.")
        else:
            print("✅ Tests passed")

    print("🎉 Done.")


if __name__ == "__main__":
    main()