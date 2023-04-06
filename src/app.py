import sys
import wx
from . import gui
from . import mkdim
from . import extract_parents

def main():
    app = wx.App()
    window =gui.MainWindow()
    window.registerTool("Make DIM",mkdim.getPanel())
    window.registerTool("Extract Parents",extract_parents.getPanel())

    window.Show()
    app.MainLoop()
