###############################################################################
# Name: ftpwindow.py                                                          #
# Purpose: Ftp Window                                                         #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Ftp Window"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx
import wx.lib.mixins.listctrl as listmix

# Editra Libraries
import ed_glob
import ed_msg
import eclib.ctrlbox as ctrlbox
import eclib.platebtn as platebtn
import eclib.elistmix as elistmix

#-----------------------------------------------------------------------------#
# Globals
ID_SITES = wx.NewId()
ID_CONNECT = wx.NewId()

_ = wx.GetTranslation

#-----------------------------------------------------------------------------#

class FtpWindow(ctrlbox.ControlBox):
    """Ftp file window"""
    def __init__(self, parent, id=wx.ID_ANY):
        ctrlbox.ControlBox.__init__(self, parent, id)

        # Attributes
        self._connected = False
        self._cbar = None     # ControlBar
        self._sites = None    # wx.Choice
        self._username = None # wx.TextCtrl
        self._password = None # wx.TextCtrl

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_PREFERENCES)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=ID_CONNECT)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, id=ID_SITES)

        # Editra Message Handlers
        ed_msg.Subscribe(self.OnThemeChanged, ed_msg.EDMSG_THEME_CHANGED)

    def __del__(self):
        """Cleanup"""
        ed_msg.Unsubscribe(self.OnThemeChanged)

    def __DoLayout(self):
        """Layout the window"""
        self._cbar = ctrlbox.ControlBar(self, style=ctrlbox.CTRLBAR_STYLE_GRADIENT)
        if wx.Platform == '__WXGTK__':
            self._cbar.SetWindowStyle(ctrlbox.CTRLBAR_STYLE_DEFAULT)

        # Preferences
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_PREF), wx.ART_MENU)
        btn = platebtn.PlateButton(self._cbar, wx.ID_PREFERENCES,
                                   bmp=bmp, style=platebtn.PB_STYLE_NOBG)
        self._cbar.AddControl(btn, wx.ALIGN_LEFT)

        # Sites
        self._cbar.AddControl(wx.StaticText(self._cbar, label=_("Sites:")), wx.ALIGN_LEFT)
        self._sites = wx.Choice(self._cbar, ID_SITES)
        self._cbar.AddControl(self._sites, wx.ALIGN_LEFT)

        # Username
        self._cbar.AddControl(wx.StaticText(self._cbar, label=_("Username:")), wx.ALIGN_LEFT)
        self._username = wx.TextCtrl(self._cbar)
        self._cbar.AddControl(self._username, wx.ALIGN_LEFT)

        # Password
        self._cbar.AddControl(wx.StaticText(self._cbar, label=_("Password:")), wx.ALIGN_LEFT)
        self._password = wx.TextCtrl(self._cbar, style=wx.TE_PASSWORD)
        self._cbar.AddControl(self._password, wx.ALIGN_LEFT)

        # Connect
        self._cbar.AddStretchSpacer()
        connect = platebtn.PlateButton(self._cbar, ID_CONNECT, label=_("Connect"))
        self._cbar.AddControl(connect, wx.ALIGN_RIGHT)

        # Setup Window
        self.SetControlBar(self._cbar, wx.TOP)
        self.SetWindow(FtpList(self, wx.ID_ANY))

    def OnButton(self, evt):
        """Handle Button click events"""
        e_id = evt.GetId()
        if e_id == ID_CONNECT:
            e_obj = evt.GetEventObject()
            if self._connected:
                self._connected = False
                # TODO: Disconnect from server
                e_obj.SetLabel(_("Connect"))
            else:
                # Connect to site
                user = self._username.GetValue().strip()
                password = self._password.GetValue().strip()
                site = self._sites.GetStringSelection()
                self._connected = True
                e_obj.SetLabel(_("Disconnect"))
            self._cbar.Layout()
        elif e_id == wx.ID_PREFERENCES:
            # Show preferences dialog
            pass
        else:
            evt.Skip()

    def OnChoice(self, evt):
        """Handle Choice Control Events"""
        if evt.GetId() == ID_SITES:
            # Change the current Site
            pass
        else:
            evt.Skip()

    def OnThemeChanged(self, msg):
        """Update icons when the theme changes
        @param msg: ed_msg.EDMSG_THEME_CHANGED

        """
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_PREF), wx.ART_MENU)
        pref = self._cbar.FindWindowById(wx.ID_PREFERENCES)
        pref.SetBitmap(bmp)
        self._cbar.Layout()

#-----------------------------------------------------------------------------#

class FtpList(listmix.ListCtrlAutoWidthMixin,
              elistmix.ListRowHighlighter,
              wx.ListCtrl):
    """Ftp File List"""
    def __init__(self, parent, id=wx.ID_ANY):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_ICON|wx.LC_REPORT) 
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        elistmix.ListRowHighlighter.__init__(self)
        self.InsertColumn(0, _("Filename"))
        self.InsertColumn(1, _("Size"))
        self.InsertColumn(2, _("Modified"))

        self.setResizeColumn(0)

