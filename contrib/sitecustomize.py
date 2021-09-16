import sys
import os
from pathlib import Path
import site

# These modifications to the 'site' module and sys.path may not work perfectly in every case.
# It is only meant to work well enough for our electron app needs

MODULE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
if sys.platform == 'win32':
    SITE_PACKAGES = MODULE_DIR / 'Lib' / 'site-packages'
else:
    SITE_PACKAGES = MODULE_DIR / 'python' / 'install' / 'lib' / 'python3.9' / 'site-packages'

site.addsitedir(str(SITE_PACKAGES))
site.USER_BASE = str(MODULE_DIR)
site.USER_SITE = str(SITE_PACKAGES)


# Remove system site-packges from sys.path
if sys.platform == 'win32':
    for_removal = set()
    for path in sys.path:
        if "Roaming" in path:
            for_removal.add(path)
else:
    for_removal = set()
    for path in sys.path:
        if ".local/lib/python" in path:
            for_removal.add(path)

for path in for_removal:
    sys.path.remove(path)


# Handle PYTHONPATH correctly
for env_var in os.environ.get('PYTHONPATH', "").split(os.pathsep):
    if env_var.strip() != "":
        sys.path.insert(0, str(Path(env_var)))

sys.path.insert(0, '')
