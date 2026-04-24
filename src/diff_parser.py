import subprocess
import re

def get_git_diff():
    result = subprocess.run(
        ["git", "diff", "--unified=0", "HEAD~1"],
        capture_output=True,
        text=True
    )
    return result.stdout


def extract_changed_functions(diff_text):
    functions = []
    pattern = re.compile(r'\+def\s+(\w+)\(.*\):')

    lines = diff_text.split("\n")
    for line in lines:
        match = pattern.search(line)
        if match:
            functions.append(match.group(1))

    return list(set(functions))