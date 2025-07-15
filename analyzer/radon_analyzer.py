import subprocess
import os

def analyze_radon(files: list[str], mode: str = "cc") -> str:
        
    command = None
    if mode == "cc":
        command = ["radon", "cc", *files, "-s", "-a"]
    elif mode == "mi":
        command = ["radon", "mi", *files, "-s"]
    elif mode == "raw":
        command = ["radon", "raw", *files]
    elif mode == "hal":
        command = ["radon", "hal", *files]
    else:
        raise ValueError("Invalid mode. Choose from 'cc', 'mi', 'hal' or 'raw'.")
    
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout if result.returncode==0 else "No output"