import wx
from . import formbuilder_gui as gui
from . import extract_parents
from . import mkdim
from dataclasses import dataclass

@dataclass
class Tool:
    name:str
    panel:wx.Panel
    button:wx.Button

class MainWindow(gui.MainWindow):
    """ creates the main window. users should add a new tool by calling registerTool(toolName,uiPanel)"""
    activeCanvas=None
    registeredTools=[]

    def __init__(self):
        super().__init__(None)

    def registerTool(self, toolName, ui_panel):
        #create the button
        box = self.m_toolbox.GetSizer()
        button = wx.Button(
            self.m_toolbox, wx.ID_ANY, toolName, wx.DefaultPosition, wx.DefaultSize, 0
        )

        #hook up canvas creation for the button
        button.Bind(wx.EVT_BUTTON, lambda x:
            self.changeCanvas(ui_panel)
            )

        #add the button to the screen
        box.Add(button, 0,  wx.EXPAND, 5)

        self.registeredTools.append(Tool(
            toolName,ui_panel,button
        ))

        #open this panel if its the only one registered
        if len(self.registeredTools)==1:
            button.ProcessEvent(wx.CommandEvent(wx.EVT_BUTTON.typeId, button.GetId()))


    def changeCanvas(self,newcanvas):
        if self.activeCanvas is not None:
            self.activeCanvas.Hide()
        canvas=self.put_drop_panel_here.GetSizer()
        if not isinstance(newcanvas,wx.Panel):
            newcanvas=newcanvas(self.put_drop_panel_here)
        canvas. Add(newcanvas, 1, wx.ALL | wx.EXPAND,0)
        self.activeCanvas=newcanvas
        self.Layout()

    def showWindow(self):
        self.Centre()
        self.Show()
