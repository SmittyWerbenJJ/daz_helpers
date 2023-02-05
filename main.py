import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from extract_parents import extract_parents
from pathlib import Path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    iconPath = Path(__file__).parent.joinpath("icons").joinpath("icon.ico")
    app.setWindowIcon(QIcon(str(iconPath)))
    mainWindow = extract_parents.MainWindow()
    sys.exit(app.exec())
