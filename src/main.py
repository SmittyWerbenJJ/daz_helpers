import sys
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from . import extract_parents
from pathlib import Path


def main():
    app = QApplication(sys.argv)
    iconPath = Path(__file__).parent.joinpath("icons").joinpath("icon.ico")
    app.setWindowIcon(QIcon(str(iconPath)))
    mainWindow = extract_parents.MainWindow()
    sys.exit(app.exec())
