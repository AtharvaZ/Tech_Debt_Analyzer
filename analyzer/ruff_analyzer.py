import subprocess

def analyze_ruff(files: list[str]):
    result = subprocess.run(["ruff", "check", *files], capture_output=True, text=True)

    if result.returncode == 0:
        return "No issues found"
    elif result.returncode == 1: 
        return result.stdout
    else:
        return result.stderr
    

