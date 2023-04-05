import sys
import wx
from . import mkdim_gui


def main(iconPath=""):
    app = wx.App()
    window =mkdim_gui.Mainwindow()
    window.showWindow()

    # try:
        # icon=wx.Icon(iconPath, wx.BITMAP_TYPE_ICO)
        # window.SetIcon(icon)
    # except Exception as e:
    #     pass
    app.MainLoop()

if __name__ == "__main__":
    sys.exit(main())
