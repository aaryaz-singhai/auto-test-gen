from test_generator import generate_tests

def fix_tests(function_name, function_code, context, error_output):
    enhanced_context = f"""
{context}

The following pytest tests are failing.

Error:
{error_output}

Fix the tests so that they pass.
Return ONLY valid Python pytest code.
No markdown. No explanation.
"""

    return generate_tests(function_name, function_code, enhanced_context)