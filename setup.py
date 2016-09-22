from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "Heisenberg.py",
            "icon_resources": [(1, "hberg.ico")]
        }
    ],
)