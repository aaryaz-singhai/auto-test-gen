import subprocess

def run_tests(test_file=None):
    cmd = ["pytest", "--maxfail=1", "--disable-warnings"]

    if test_file:
        cmd.append(test_file)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    return {
        "passed": result.returncode == 0,
        "output": result.stdout + result.stderr
    }