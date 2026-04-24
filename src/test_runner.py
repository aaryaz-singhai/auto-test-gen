import subprocess

def run_tests():
    result = subprocess.run(
        ["pytest", "--maxfail=1", "--disable-warnings"],
        capture_output=True,
        text=True
    )

    return {
        "passed": result.returncode == 0,
        "output": result.stdout + result.stderr
    }