# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 730,618 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel6, wx.ID_ANY, u"Tools" ), wx.VERTICAL )

		self.m_toolbox = wx.Panel( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TAB_TRAVERSAL )
		self.m_toolbox.SetMinSize( wx.Size( 100,-1 ) )
		self.m_toolbox.SetMaxSize( wx.Size( 100,-1 ) )

		toolboxSizer = wx.BoxSizer( wx.VERTICAL )


		self.m_toolbox.SetSizer( toolboxSizer )
		self.m_toolbox.Layout()
		sbSizer1.Add( self.m_toolbox, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( sbSizer1, 0, wx.ALL|wx.EXPAND, 5 )

		the_content = wx.StaticBoxSizer( wx.StaticBox( self.m_panel6, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )

		self.put_drop_panel_here = wx.Panel( the_content.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )


		self.put_drop_panel_here.SetSizer( bSizer16 )
		self.put_drop_panel_here.Layout()
		bSizer16.Fit( self.put_drop_panel_here )
		the_content.Add( self.put_drop_panel_here, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( the_content, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel6.SetSizer( bSizer1 )
		self.m_panel6.Layout()
		bSizer1.Fit( self.m_panel6 )
		bSizer10.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 0 )


		self.SetSizer( bSizer10 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


