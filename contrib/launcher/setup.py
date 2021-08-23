"""Run: pyinstaller --console -F electrumsv-sdk.py to create the standalone exe """

from distutils.core import setup
setup(
    console = [
        {
            "script": 'electrumsv-sdk.py',
            "icon_resources": [(1, "electrum-sv.ico")]
        }
    ]
)
