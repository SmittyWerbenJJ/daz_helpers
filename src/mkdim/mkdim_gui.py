import wx
import wx.lib.dialogs
import wx.adv
from pathlib import Path

from .progressReport import ProgressReport, MessageType
from . import gui, mkdim


ID_CopyBtn = wx.NewIdRef()
ID_PasteBtn = wx.NewIdRef()
ID_BitmapBtn = wx.NewIdRef()

def getPanel():
    return FileDropPanel

def playToastMessage(parent, title: str, message: str, iconflags=wx.ICON_INFORMATION):
    notify = wx.adv.NotificationMessage(
        title=title, message=message, parent=parent, flags=iconflags
    )
    notify.Show(timeout=5)  # 1 for short timeout, 100 for long timeout
    notify.Close()  # Hides the notification.


class FileDropPanel(gui.panel_MakeDim, wx.FileDropTarget):
    class DropTarget(wx.FileDropTarget):
        def __init__(self):
            super().__init__()

    parentFrame: wx.Frame = None

    def __init__(self, parent):
        super().__init__(parent)
        self.dropTarget = FileDropPanel.DropTarget()
        self.dropTarget.OnDropFiles = self.OnDropFiles

        self.dropBox.SetDropTarget(self.dropTarget)
        self.filepaths = []
        self.destDirText.SetHint(
            "Select Destination Director. (Leave emtpy to Build next to the File)"
        )
        self.SetAutoLayout(True)

    def OnDropFiles(self, x, y, filenames):
        self.filepaths = list(set(self.filepaths + filenames))
        self.dropBox.Clear()
        self.dropBox.AppendItems(self.filepaths)
        return True

    def OnDestDirTextChanged(self, event):
        self.dstDirPickerCtrl.SetPath(self.destDirText.GetValue())

    def onSelectDestinationFolder(self, event):
        super().onSelectDestinationFolder(event)
        givenDir = self.dstDirPickerCtrl.GetPath()
        if Path(givenDir).exists():
            self.destDirText.SetValue(givenDir)

    def onClear(self, event):
        self.dropBox.Clear()
        self.filepaths.clear()

    def on_makeIM(self, event):
        """Start creating Install Manager Files"""
        filepaths = self.filepaths

        if len(filepaths) == 0:
            return
        ProgressDialog(self, "Processing Files...", maximum=len(filepaths))

        thread = mkdim.mkdimThread(
            filepaths, self.dstDirPickerCtrl.GetPath(), ProgressDialog.onReport
        )
        thread.start()


class ProgressDialog(wx.ProgressDialog):
    instance = None

    def __init__(
        self,
        parent,
        title,
        maximum=100,
    ):
        super().__init__(title, "", maximum, parent)
        ProgressDialog.instance = self

    @classmethod
    def onReport(cls, progressReport: ProgressReport):
        if ProgressDialog.instance is None:
            return
        newValue = ProgressDialog.instance.GetValue()
        message = ""
        match = progressReport.messageType
        if match == MessageType.INFO:
            message = progressReport.message

        elif match == MessageType.FINISHED_ONE:
            message += progressReport.message
            newValue += 1
        elif match == MessageType.FINISHED_COMPLETELY:
            ProgressDialog.Shutdown()

        formattedMessage = "[{}/{}] {}".format(
            min(newValue, ProgressDialog.instance.GetRange()),
            ProgressDialog.instance.GetRange(),
            message,
        )
        message = formattedMessage
        ProgressDialog.instance.Update(newValue, message)

    @classmethod
    def Shutdown(cls):
        playToastMessage(
            ProgressDialog.instance,
            "Conversion Done",
            f"Finished Converting {ProgressDialog.instance.GetRange()} items",
        )
        ProgressDialog.instance.Destroy()
