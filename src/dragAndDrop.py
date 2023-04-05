import wx

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, listbox: wx.ListBox):
        wx.FileDropTarget.__init__(self)
        self.listbox = listbox
        self.filepaths = []

    def OnDropFiles(self, x, y, filenames):
        self.filepaths = list(set(self.filepaths + filenames))
        self.listbox.Clear()
        self.listbox.AppendItems(self.filepaths)
        return True

    def getDroppedFiles(self):
        return self.listbox.GetItems()
