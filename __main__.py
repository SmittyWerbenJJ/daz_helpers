import os
import sys
import src

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cwd)
os.chdir(cwd)


if __name__ == "__main__":
    iconPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons\\icon.ico")
    sys.exit(src.app.main(iconPath=iconPath))
