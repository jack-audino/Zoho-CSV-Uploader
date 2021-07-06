'''
When converting this project to an exe file via PyInstaller, the file path of config/config.txt is changed, which would normally
crash the program, however, this function allows for the path to be translated so the program can still use it

This code is from a solution on stackoverflow:
https://stackoverflow.com/questions/39885354/pyinstaller-cannot-add-txt-files
'''
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2",os.path.abspath("."))

    return os.path.join(base_path, relative_path)