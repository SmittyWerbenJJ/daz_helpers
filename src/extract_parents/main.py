from . import extract_parents
import wx

def getPanel()-> wx.Panel:
    """ return this panel when running from the main app"""
    return extract_parents.MainPanel

def runAsMAin():
    """ run as Main App"""
    import wx
    import sys
    app=wx.App()
    window=wx.Frame()
    window.SetSizer(wx.BoxSizer(wx.VERTICAL))
    panel= extract_parents.MainPanel(window)
    window.GetSizer().add(panel)
    window.show()
    sys.exit(app.MainLoop())

if __name__=="__main__":
    runAsMAin()
