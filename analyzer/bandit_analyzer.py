import subprocess
import json

def analyze_bandit(files: list[str]) -> str:
    result = subprocess.run(
        ["bandit", "-r", *files, "-f", "json"],
        capture_output=True,
        text=True
    )
    return result.stdout if result.returncode==0 else "No issues identified"