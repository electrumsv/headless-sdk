import sys
import os
from pathlib import Path

for env_var in os.environ.get('PYTHONPATH', "").split(";"):
    if env_var.strip() != "":
        sys.path.insert(0, str(Path(env_var)))

sys.path.insert(0, '')

