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

		bSizer42 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		bSizer11.SetMinSize( wx.Size( 200,-1 ) )
		self.m_caption = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Processing ...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_caption.Wrap( -1 )

		bSizer11.Add( self.m_caption, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_label_progress = wx.StaticText( self.m_panel6, wx.ID_ANY, u"001 / 500", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_label_progress.Wrap( -1 )

		bSizer11.Add( self.m_label_progress, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_progressbar = wx.Gauge( self.m_panel6, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_progressbar.SetValue( 0 )
		bSizer11.Add( self.m_progressbar, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer42.Add( bSizer11, 1, wx.EXPAND, 5 )


		bSizer38.Add( bSizer42, 1, wx.EXPAND, 5 )

		bSizer111 = wx.BoxSizer( wx.VERTICAL )

		self.m_textbox = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,200 ), wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer111.Add( self.m_textbox, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer38.Add( bSizer111, 0, wx.EXPAND, 5 )

		m_buttons = wx.StdDialogButtonSizer()
		self.m_buttonsCancel = wx.Button( self.m_panel6, wx.ID_CANCEL )
		m_buttons.AddButton( self.m_buttonsCancel )
		m_buttons.Realize();

		bSizer38.Add( m_buttons, 0, wx.EXPAND, 5 )


		self.m_panel6.SetSizer( bSizer38 )
		self.m_panel6.Layout()
		bSizer38.Fit( self.m_panel6 )
		bSizer33.Add( self.m_panel6, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer33 )
		self.Layout()
		bSizer33.Fit( self )

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


