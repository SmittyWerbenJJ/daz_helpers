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

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel6, wx.ID_ANY, u"label" ), wx.VERTICAL )

		self.m_toolbox = wx.ScrolledWindow( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.m_toolbox.SetScrollRate( 5, 5 )
		toolboxSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_button4 = wx.Button( self.m_toolbox, wx.ID_ANY, u"MakeDim", wx.DefaultPosition, wx.DefaultSize, 0 )
		toolboxSizer.Add( self.m_button4, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_toolbox.SetSizer( toolboxSizer )
		self.m_toolbox.Layout()
		sbSizer1.Add( self.m_toolbox, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( sbSizer1, 0, wx.EXPAND, 10 )

		the_content = wx.StaticBoxSizer( wx.StaticBox( self.m_panel6, wx.ID_ANY, u"label" ), wx.VERTICAL )

		self.put_drop_panel_here = wx.Panel( the_content.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )


		self.put_drop_panel_here.SetSizer( bSizer16 )
		self.put_drop_panel_here.Layout()
		bSizer16.Fit( self.put_drop_panel_here )
		the_content.Add( self.put_drop_panel_here, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( the_content, 1, wx.EXPAND, 5 )


		self.m_panel6.SetSizer( bSizer1 )
		self.m_panel6.Layout()
		bSizer1.Fit( self.m_panel6 )
		bSizer10.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 0 )


		self.SetSizer( bSizer10 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button4.Bind( wx.EVT_BUTTON, self.OnOpenPanel_MakeDim )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnOpenPanel_MakeDim( self, event ):
		event.Skip()


###########################################################################
## Class panel_MakeDim
###########################################################################

class panel_MakeDim ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Drag some files here:", wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_staticText1.Wrap( -1 )

		bSizer14.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )

		dropBoxChoices = []
		self.dropBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dropBoxChoices, 0 )
		bSizer14.Add( self.dropBox, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.destDirText = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.destDirText, 1, wx.ALL|wx.EXPAND, 5 )

		self.dstDirPickerCtrl = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DIR_MUST_EXIST )
		bSizer8.Add( self.dstDirPickerCtrl, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer14.Add( bSizer8, 0, wx.EXPAND, 5 )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_build = wx.Button( self, wx.ID_ANY, u"Build", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.btn_build, 1, wx.ALL, 5 )

		self.btn_clear = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.btn_clear, 0, wx.ALL, 5 )


		bSizer14.Add( bSizer18, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer14 )
		self.Layout()

		# Connect Events
		self.destDirText.Bind( wx.EVT_TEXT, self.OnDestDirTextChanged )
		self.dstDirPickerCtrl.Bind( wx.EVT_DIRPICKER_CHANGED, self.onSelectDestinationFolder )
		self.btn_build.Bind( wx.EVT_BUTTON, self.on_makeIM )
		self.btn_clear.Bind( wx.EVT_BUTTON, self.onClear )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnDestDirTextChanged( self, event ):
		event.Skip()

	def onSelectDestinationFolder( self, event ):
		event.Skip()

	def on_makeIM( self, event ):
		event.Skip()

	def onClear( self, event ):
		event.Skip()


###########################################################################
## Class ProgressDialog
###########################################################################

class ProgressDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer33 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer38 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel7 = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer42 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer11.SetMinSize( wx.Size( 200,-1 ) )
		self.spinner = wx.ActivityIndicator(self.m_panel7)
		bSizer11.Add( self.spinner, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_label_Processing = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Processing ...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_label_Processing.Wrap( -1 )

		bSizer11.Add( self.m_label_Processing, 1, wx.ALL, 5 )

		self.m_label_progress = wx.StaticText( self.m_panel7, wx.ID_ANY, u"001 / 500", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_label_progress.Wrap( -1 )

		bSizer11.Add( self.m_label_progress, 0, wx.ALL, 5 )


		bSizer42.Add( bSizer11, 1, wx.EXPAND, 5 )

		self.m_label_progress_CurrentPackage = wx.StaticText( self.m_panel7, wx.ID_ANY, u"Package.001-Package.001Package.001Package.001", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_label_progress_CurrentPackage.Wrap( -1 )

		bSizer42.Add( self.m_label_progress_CurrentPackage, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_gauge_progress = wx.Gauge( self.m_panel7, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge_progress.SetValue( 0 )
		bSizer42.Add( self.m_gauge_progress, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel7.SetSizer( bSizer42 )
		self.m_panel7.Layout()
		bSizer42.Fit( self.m_panel7 )
		bSizer38.Add( self.m_panel7, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_collapsiblePane1 = wx.CollapsiblePane( self.m_panel6, wx.ID_ANY, u"collapsible", wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE )
		self.m_collapsiblePane1.Collapse( True )

		bSizer67 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel8 = wx.Panel( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_radio_progress1 = wx.RadioButton( self.m_panel8, wx.ID_ANY, u"RadioBtn", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radio_progress1.Enable( False )

		bSizer12.Add( self.m_radio_progress1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radio_progress2 = wx.RadioButton( self.m_panel8, wx.ID_ANY, u"RadioBtn", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radio_progress2.Enable( False )

		bSizer12.Add( self.m_radio_progress2, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radio_progress3 = wx.RadioButton( self.m_panel8, wx.ID_ANY, u"RadioBtn", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radio_progress3.Enable( False )

		bSizer12.Add( self.m_radio_progress3, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radio_progress4 = wx.RadioButton( self.m_panel8, wx.ID_ANY, u"RadioBtn", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radio_progress4.Enable( False )

		bSizer12.Add( self.m_radio_progress4, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel8.SetSizer( bSizer12 )
		self.m_panel8.Layout()
		bSizer12.Fit( self.m_panel8 )
		bSizer67.Add( self.m_panel8, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_collapsiblePane1.GetPane().SetSizer( bSizer67 )
		self.m_collapsiblePane1.GetPane().Layout()
		bSizer67.Fit( self.m_collapsiblePane1.GetPane() )
		bSizer38.Add( self.m_collapsiblePane1, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel6.SetSizer( bSizer38 )
		self.m_panel6.Layout()
		bSizer38.Fit( self.m_panel6 )
		bSizer33.Add( self.m_panel6, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizer33 )
		self.Layout()
		bSizer33.Fit( self )

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


