"""
With embedded python distributions the setup.py does not produce a funtional electrumsv-sdk.exe.
Therefore we need to create one ourselves using PyInstaller (the simplest method I could muster).
This is merely a basic wrapper for calling the __main__.py and feeding it the sys.argv commandline
arguments.

Note the environment variables SDK_POSTGRES_PORT & SDK_PORTABLE must be set for the self-contained /
headless SDK distribution.
"""

import subprocess
import sys
from pathlib import Path
import os

os.environ['SDK_POSTGRES_PORT'] = "5432"
os.environ['SDK_PORTABLE_MODE'] = "1"

MODULE_DIR = Path(os.path.dirname(os.path.abspath(sys.executable)))
PYTHON_EXE = str(MODULE_DIR / "python" / 'python.exe')
SDK_MAIN_ENTRYPOINT = str(MODULE_DIR / "python" / "Lib" / "site-packages" / "electrumsv_sdk" / "__main__.py")
cmd = [PYTHON_EXE, SDK_MAIN_ENTRYPOINT]
cmd.extend(sys.argv[1:])

# print(f"MODULE_DIR={MODULE_DIR}")
# print(PYTHON_EXE)
# print(SDK_MAIN_ENTRYPOINT)
# print(cmd)

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
