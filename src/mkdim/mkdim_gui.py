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
        dialog = ProgressDialog(self, "Processing Files...", maximum=len(filepaths))
        thread = mkdim.mkdimThread(
            filepaths, self.dstDirPickerCtrl.GetPath(), dialog.update
        )
        thread.start()
        dialog.ShowModal()


class ProgressDialog(gui.ProgressDialog):
    instance = None

    def __init__(
        self,
        parent,
        title,
        maximum=100,
    ):

        super().__init__(parent)
        ProgressDialog.instance = self
        self.errorMessages=[]
        self.current=0
        self.maxValue=maximum
        self.m_progressbar.SetRange(maximum)
        self.current_item=""

    def update(self, progressReport: ProgressReport):
        newValue =self.current
        match = progressReport.messageType
        message=progressReport.message
        statusMessage=""
        doShutdown=False

        if match == MessageType.START:
            self.current_item=progressReport.message
        if match == MessageType.INFO:
            statusMessage=progressReport.message
        elif match == MessageType.FINISHED_ONE:
            self.current += 1
        elif match == MessageType.FINISHED_COMPLETELY:
            statusMessage=""
            doShutdown=True
        elif match==MessageType.ERROR:
            self.errorMessages.append(message)
            statusMessage="ERROR"

        formattedProgressLabel="{:03d}/{:03d}".format(
            self.current,self.maxValue
        )

        self.m_caption.SetLabel(f"Processing {self.current_item}...")
        self.m_progressbar.SetValue(newValue)
        self.m_label_progress.SetLabel(formattedProgressLabel)
        if statusMessage!="":
            self.m_textbox.AppendText(statusMessage+"\n")

        if doShutdown:
            self.m_textbox.AppendText("\n".join(self.errorMessages))
            self.Shutdown()

    def Shutdown(self):
        errors=self.errorMessages
        if len(errors)==0:
            playToastMessage(
                self.GetParent(),
                "Conversion Done",
                f"Finished Converting {self.maxValue} items",
            )
            self.Destroy()
        else:
            playToastMessage(
            self.GetParent(),
            "Conversion Done",
            f"Some Errors hav occured during Conversions. 👀",
            wx.ICON_ERROR
             )
