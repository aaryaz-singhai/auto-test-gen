from test_generator import generate_tests

def fix_tests(function_name, function_code, context, error_output):
    prompt = f"""
The following pytest tests are failing.

Error:
{error_output}

Fix the tests.

Function:
{function_code}

Context:
{context}
"""

    return generate_tests(function_name, function_code, context)