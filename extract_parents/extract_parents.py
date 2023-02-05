import sys
import pyperclip
from typing import Optional
import tempfile
import subprocess
from pathlib import Path

from PySide6.QtWidgets import *  # QApplication, QDialog, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget
from PySide6.QtCore import *


from . import everything_utils
from .ui import ui_main, ui_dialog


def open_paths_in_everything(paths: list[Path]):
    try:
        _, tmpfile = tempfile.mkstemp(suffix=".efu")
        everything_path = r'C:\Program Files\Everything\Everything.exe'
        command = fr'"{everything_path}" "{tmpfile}"'
        everything_utils.write_paths_to_efu(paths, Path(tmpfile))
        print(f"running {command} ...")
        if not Path(everything_path).exists:
            raise FileNotFoundError(f"Everything is not Installed!\n{everything_path}")
        subprocess.Popen(command)
    except Exception as e:
        QMessageBox.critical(
            None,
            "Error opening everything",
            str(e),
            QMessageBox.StandardButton.Close
        )

    # subprocess.Popen(fr'explorer /select,"file:///{file_path}"')


class ResultDialog(QDialog):
    file_paths: list[Path]

    def __init__(self, parent, file_paths: list[Path]) -> None:
        super().__init__(parent, Qt.WindowType.Dialog)
        self.file_paths = file_paths
        self.ui = ui_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        for path in self.file_paths:
            self.ui.listbox.addItem(str(path))
        self.exec()

    def contextMenuEvent(self, event):
        contextMenu = QMenu()
        contextMenu.addAction("open in Everything", self.on_listbox_rclick)
        contextMenu.exec(self.mapToGlobal(event.pos()))

    def getFilePathsFromListBox(self, onlySelected=False):
        paths = []
        if onlySelected:
            listitems = self.ui.listbox.selectedItems()
        else:
            listitems = [self.ui.listbox.item(i) for i in range(self.ui.listbox.count())]

        for line in listitems:
            path = Path(line.text())
            if path.exists():
                paths.append(path)
        return paths

    def on_listbox_rclick(self):
        file_paths = self.getFilePathsFromListBox(onlySelected=True)
        print(file_paths[:3])

    @Slot()
    def select_all(self):
        self.ui.listbox.selectAll()

    @Slot()
    def select_invert(self):
        for i in range(self.ui.listbox.count()):
            item = self.ui.listbox.item(i)
            item.setSelected(not item.isSelected())

    @Slot()
    def select_none(self):
        for item in self.ui.listbox.selectedItems():
            item.setSelected(False)

    def copy_To_Clipboard(self):
        pyperclip.copy(self.getFilePathsFromListBox(True))

    @Slot()
    def open_all_in_everything(self):
        file_paths = self.getFilePathsFromListBox()
        open_paths_in_everything(file_paths)

    @Slot()
    def open_selected_in_everything(self):
        file_paths = self.getFilePathsFromListBox(onlySelected=True)
        open_paths_in_everything(file_paths)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Extract Parent Paths")
        self.show()

    @Slot(str)
    def getParentPath(self, sender):
        parent_paths = []
        for line in self.ui.inputbox.toPlainText().splitlines():
            path = Path(line)
            if path.exists:
                parent_paths.append(path.parent)

        ResultDialog(self, list(map(Path, parent_paths)))

    @Slot()
    def open_all_in_everything(self):
        file_paths = self.getFilePathsFromTextBox()
        open_paths_in_everything(file_paths)

    def getFilePathsFromTextBox(self):
        paths = []
        for path in map(Path, self.ui.inputbox.toPlainText().splitlines()):
            if path.exists():
                paths.append(path)
        return paths
