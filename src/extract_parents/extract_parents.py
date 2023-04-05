
import tempfile
import subprocess
from pathlib import Path
import wx,wx.adv
from . import everything_utils


def open_paths_in_everything(paths: list[Path]):
    try:
        _, tmpfile = tempfile.mkstemp(suffix=".efu")
        everything_path=everything_utils.everything_path
        command = fr'"{everything_path}" "{tmpfile}"'
        everything_utils.write_paths_to_efu(paths, Path(tmpfile))
        print(f"running {command} ...")
        if not Path(everything_path).exists:
            raise FileNotFoundError(f"Everything is not Installed!\n{everything_path}")
        subprocess.Popen(command)
    except Exception as e:
        wx.MessageBox(
            f"Error opening everything:\n{str(e)}",
            "Error opening everything",
            wx.OK_DEFAULT|wx.ICON_ERROR
        )

def getClenedPath(path:str):
    return path.strip().replace("\"","").strip()


parent_paths=[]

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer=wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.textbox=wx.TextCtrl(self,wx.ID_ANY,style=wx.TE_MULTILINE|wx.TE_DONTWRAP)
        sizer.Add(self.textbox,1,wx.ALL|wx.EXPAND,5)

        groupbox=wx.StaticBoxSizer(wx.VERTICAL,self,"Options")
        sizer.Add(groupbox,0,wx.ALL|wx.EXPAND,5)

        btn_getParentPaths=wx.Button(self,wx.ID_ANY,"Get Parent Paths")
        btn_getParentPaths.Bind(wx.EVT_BUTTON,self.OnGetParentPath)
        groupbox.Add(btn_getParentPaths,1,wx.ALL|wx.EXPAND,5)
        btn_openInEverything=wx.Button(self,wx.ID_ANY,"Open in Everything")
        groupbox.Add(btn_openInEverything,1,wx.ALL|wx.EXPAND,5)

    def OnGetParentPath(self,sender):
        for path in [Path(getClenedPath(x)) for x in self.textbox.GetValue().splitlines()]:
            if path.exists:
                parent_paths.append(path.parent)
        ParentPathsDialog(self, list(map(Path, parent_paths)))



class ParentPathsDialog(wx.Dialog):
    def __init__(self,parent,paths:list[Path]):
        super().__init__(parent, wx.ID_ANY, "Parent paths",size=(500,500), style=wx.DEFAULT_DIALOG_STYLE)

        self.file_paths = paths
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.listbox=wx.ListBox(self,style=wx.LB_EXTENDED)
        self.listbox.InsertItems([str(p) for p in self.file_paths],0)
        sizer.Add(self.listbox,1,wx.ALL|wx.EXPAND,5)

        groupbox=wx.StaticBoxSizer(wx.VERTICAL,self,"Options")
        sizer.Add(groupbox,0,wx.ALL|wx.EXPAND,5)

        grpbox_layer0=wx.BoxSizer(wx.HORIZONTAL)
        grpbox_layer1=wx.BoxSizer(wx.HORIZONTAL)
        groupbox.Add(grpbox_layer0,1,wx.EXPAND|wx.ALL,0)
        groupbox.Add(grpbox_layer1,1,wx.EXPAND|wx.ALL,0)

        btn_selectAll=wx.Button(self,wx.ID_ANY,"Select: All")
        btn_selectAll.Bind( wx.EVT_BUTTON, self.select_all )

        btn_selectNone=wx.Button(self,wx.ID_ANY,"Select: None")
        btn_selectNone.Bind( wx.EVT_BUTTON, self.select_none )

        btn_selectInvert=wx.Button(self,wx.ID_ANY,"Select: Invert")
        btn_selectInvert.Bind( wx.EVT_BUTTON, self.select_invert )
        for btn in [btn_selectAll,btn_selectNone,btn_selectInvert]:
            grpbox_layer0.Add(btn,1,wx.EXPAND|wx.ALL,5)


        btn_OpenAll=wx.Button(self,wx.ID_ANY,"Open: All In Everything")
        btn_OpenAll.Bind( wx.EVT_BUTTON, self.open_all_in_everything )
        btn_OpenSelected=wx.Button(self,wx.ID_ANY,"Open: Selected")
        btn_OpenSelected.Bind( wx.EVT_BUTTON, self.open_selected_in_everything )
        btn_CopyToClipboard=wx.Button(self,wx.ID_ANY,"Copy AllTo Clipboard")
        btn_CopyToClipboard.Bind( wx.EVT_BUTTON, self.copy_To_Clipboard )

        for btn in [btn_OpenAll,btn_OpenSelected,btn_CopyToClipboard]:
            grpbox_layer1.Add(btn,1,wx.EXPAND|wx.ALL,5)

        self.SetSizer(sizer)
        self.Layout()
        self.Show()


    def getFilePathsFromListBox(self, onlySelected=False):
        if onlySelected:
            listitems=[self.listbox.GetString(i) for i in self.listbox.GetSelections() ]
        else:
            listitems = [self.listbox.GetString(i) for i in range(self.listbox.GetCount())]

        #clean them paths
        listitems=list(map(getClenedPath,listitems))
        return [Path(x) for x in listitems ]

    def select_all(self,evt):
        for i in range(self.listbox.GetCount()):
            self.listbox.SetSelection(i)




    def select_invert(self,evt):
        old_selections=self.listbox.GetSelections()
        self.listbox.SetSelection(wx.NOT_FOUND)

        for i in range(self.listbox.GetCount()):
            if i not in old_selections:
                self.listbox.SetSelection(i)


    def select_none(self,evt):
        self.listbox.SetSelection(wx.NOT_FOUND)


    def copy_To_Clipboard(self,evt):
        lines=[]
        for item in range(self.listbox.Count):
            lines.append(self.listbox.GetString(item))
        x="\n".join(lines)
        # Write some text to the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(x))
            wx.TheClipboard.Close()


    def open_all_in_everything(self,evt):
        file_paths = self.getFilePathsFromListBox()
        open_paths_in_everything(file_paths)

    def open_selected_in_everything(self,evt):
        file_paths = self.getFilePathsFromListBox(onlySelected=True)
        open_paths_in_everything(file_paths)
