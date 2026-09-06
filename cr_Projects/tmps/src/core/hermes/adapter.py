# REAL HERMES ADAPTER — no mocks
import subprocess, shlex
def send(prompt):
    return subprocess.run(["hermes","-z",prompt,"--cli"], capture_output=True, text=True).stdout
