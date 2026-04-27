import os
import ast
from diff_parser import get_git_diff, extract_changed_functions
from context_builder import extract_function_code, extract_imports
from test_generator import generate_tests
from test_runner import run_tests
from feedback_loop import fix_tests

SOURCE_FILE = "sample.py"


def save_test_file(function_name, test_code):
    os.makedirs("tests", exist_ok=True)
    file_path = f"tests/test_{function_name}.py"

    with open(file_path, "w") as f:
        f.write(test_code)

    return file_path


def is_valid_python(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def main():
    print("🔍 Detecting changes...")
    diff = get_git_diff(SOURCE_FILE)
    functions = extract_changed_functions(diff)

    if not functions:
        print("No new functions detected.")
        return

    print(f"🧠 Functions found: {functions}")

    imports = extract_imports(SOURCE_FILE)
    function_map = extract_function_code(SOURCE_FILE, functions)

    for fn_name, fn_code in function_map.items():
        print(f"\n⚙️ Generating tests for {fn_name}...")

        # --- Generate valid test code ---
        for attempt in range(3):
            test_code = generate_tests(fn_name, fn_code, imports)

            if is_valid_python(test_code):
                break
            else:
                print(f"[Retry {attempt+1}] Invalid syntax from LLM")

        else:
            print("❌ Could not generate valid test code")
            continue

        save_test_file(fn_name, test_code)

        print(f"🧪 Running tests for {fn_name}...")
        result = run_tests()

        if not result["passed"]:
            print("❌ Tests failed. Attempting fix...")

            # --- Fix loop with error feedback ---
            for attempt in range(3):
                fixed_code = fix_tests(
                    fn_name,
                    fn_code,
                    imports,
                    result["output"]
                )

                if not is_valid_python(fixed_code):
                    print(f"[Retry {attempt+1}] Fix produced invalid syntax")
                    continue

                save_test_file(fn_name, fixed_code)
                result = run_tests()

                if result["passed"]:
                    print("✅ Tests fixed successfully")
                    break

            else:
                print("⚠️ Still failing. Manual review needed.")
        else:
            print("✅ Tests passed")

    print("\n🎉 Done.")

    # print("---- TEST ERROR ----")
    print(result["output"])
    print("--------------------")


if __name__ == "__main__":
    main()