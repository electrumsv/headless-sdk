import subprocess
import sys
from pathlib import Path
import os
import platform

VERSION = "0.0.6"


def load_dotenv(env_path):
    """Avoids 3rd party 'dotenv' dependency because it significantly bloats the final exe and
    makes the startup time slow (pyinstaller --onefile option copies all files to a
    temp location each time it is called)"""

    with open(env_path, 'r') as f:
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
        process = subprocess.Popen(cmd, env=os.environ.copy())
        if process:
            process.wait()
    except KeyboardInterrupt:
        if process:
            process.terminate()
            process.wait()
    finally:
        sys.exit(0)


if sys.platform == "win32":
    MODULE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    ENV_PATH = MODULE_DIR.parent.parent / ".env"
    PYTHON_EXE = str(MODULE_DIR.parent / 'python.exe')
    SDK_MAIN_ENTRYPOINT = str(
        MODULE_DIR.parent / "Lib" / "site-packages" / "electrumsv_sdk" / "__main__.py")
    cmd = [PYTHON_EXE, SDK_MAIN_ENTRYPOINT]
    cmd.extend(sys.argv[1:])
    load_dotenv(ENV_PATH)
else:
    MODULE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    ENV_PATH = MODULE_DIR.parent.parent.parent / ".env"
    PYTHON_EXE = str(MODULE_DIR / 'python3')
    PYTHON_MAJOR_VERSION = platform.python_version().split('.')[1]
    SDK_MAIN_ENTRYPOINT = str(
        MODULE_DIR.parent / "lib" / f"python3.{PYTHON_MAJOR_VERSION}" / "site-packages" / "electrumsv_sdk" / "__main__.py")
    cmd = [PYTHON_EXE, SDK_MAIN_ENTRYPOINT]
    cmd.extend(sys.argv[1:])
    load_dotenv(ENV_PATH)

# # Debugging
# print(f"MODULE_DIR={MODULE_DIR}")
# print(env_path)
# print(PYTHON_EXE)
# print(SDK_MAIN_ENTRYPOINT)
# print(cmd)
# print(f"os.environ['SDK_POSTGRES_PORT']={os.environ['SDK_POSTGRES_PORT']}")
# print(f"os.environ['SDK_PORTABLE_MODE']={os.environ['SDK_PORTABLE_MODE']}")

launch_sdk()
