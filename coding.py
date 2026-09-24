import subprocess
import sys
import time

PROGRAM = "code.py"

while True:
    try:
        subprocess.run(["git", "fetch"], check=True)

        local = subprocess.check_output(
            ["git", "rev-parse", "HEAD"]
        ).decode().strip()

        remote = subprocess.check_output(
            ["git", "rev-parse", "@{u}"]
        ).decode().strip()

        if local != remote:
            print("Update found!")
            subprocess.run(["git", "pull"], check=True)
            print("Updated.")

        print("Starting program...")
        subprocess.run([sys.executable, PROGRAM])

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
