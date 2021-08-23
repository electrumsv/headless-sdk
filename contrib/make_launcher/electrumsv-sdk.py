"""
With embedded python distributions the setup.py does not produce a functional electrumsv-sdk.exe.
Therefore we need to create a very lightweight executable launcher
(the simplest method I could muster).
"""

import subprocess
import sys
from pathlib import Path
import os


def load_dotenv(ENV_PATH):
    """Avoids 3rd party 'dotenv' dependency because it significantly bloats the final exe and
    makes the startup time slow (pyinstaller --onefile option copies all files to a
    temp location each time it is called)"""

    with open(ENV_PATH, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # comments
            if line.startswith("#"):
                continue
            if "=" in line:
                key = line.split("=")[0].strip()
                val = line.split("=")[1].strip()
                os.environ[key] = val


def launch_sdk():
    process = None
    try:
        if sys.platform == 'win32':
            process = subprocess.Popen(cmd, env=os.environ.copy())
        elif sys.platform in {'linux', 'darwin'}:
            process = subprocess.Popen(f"{cmd}", shell=True, env=os.environ.copy())

        if process:
            process.wait()
    except KeyboardInterrupt:
        if process:
            process.terminate()
            process.wait()
    finally:
        sys.exit(0)


MODULE_DIR = Path(os.path.dirname(os.path.abspath(sys.executable)))
ENV_PATH = MODULE_DIR / ".env"
PYTHON_EXE = str(MODULE_DIR / "python" / 'python.exe')
SDK_MAIN_ENTRYPOINT = str(MODULE_DIR / "python" / "Lib" / "site-packages" / "electrumsv_sdk" / "__main__.py")
cmd = [PYTHON_EXE, SDK_MAIN_ENTRYPOINT]
cmd.extend(sys.argv[1:])
load_dotenv(ENV_PATH)

# # Debugging
# print(f"MODULE_DIR={MODULE_DIR}")
# print(ENV_PATH)
# print(PYTHON_EXE)
# print(SDK_MAIN_ENTRYPOINT)
# print(cmd)
# print(f"os.environ['SDK_POSTGRES_PORT']={os.environ['SDK_POSTGRES_PORT']}")
# print(f"os.environ['SDK_PORTABLE_MODE']={os.environ['SDK_PORTABLE_MODE']}")

launch_sdk()
