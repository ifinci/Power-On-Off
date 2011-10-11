'''
    powerOnOff.py
    
    INTRODUCTION:
        This module implements the graphical UI of the application, and uses
        the ipc.py module for actually controling the device.
        
    CHANGE LOG:
'''
__version__ = '2.0'
__author__ = "Ilan Finci (Ilan@Finci.org)"
__date__ = '11-Oct-2011'

__info__ = '''
    Version: ''' + __version__ + '''
    Author: ''' + __author__ + '''
    Date: ''' + __date__ + '''
'''

import wx

from ipc import IPC

menu_ABOUT = wx.NewId()

class PooFrame(wx.Frame):
    '''
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    '''
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(200, 150))

        # instance of the IPC we control.
        self._ipc=IPC("COM1")
                          
        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")

        #add help menu
        help_menu = wx.Menu()
        help_menu.Append(menu_ABOUT, "&About\tAlt-A", "About this application")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=menu_ABOUT)
        menuBar.Append(help_menu, "&Help")


        self.SetMenuBar(menuBar)

        #self.CreateStatusBar()
        

        # Now create the Panel to put the other controls on.
        self.panel = wx.Panel(self)

        # and a few controls
        text = wx.StaticText(self.panel, -1, "Power On Off")
        text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        self.on_btn = wx.Button(self.panel, -1, "On")
        self.off_btn = wx.Button(self.panel, -1, "Off")

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnONButton, self.on_btn)
        self.Bind(wx.EVT_BUTTON, self.OnOFFButton, self.off_btn)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, 10)
        
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.on_btn, 0, wx.ALL, 1)
        sizer2.Add(self.off_btn, 0, wx.ALL, 1)
        sizer.Add(sizer2, 0, wx.ALL| wx.ALIGN_CENTRE_HORIZONTAL, 10)
        self.panel.SetSizer(sizer)
        self.panel.Layout()
        
        #add icon
        _icon = wx.Icon('resources\\acc.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(_icon)

    def OnTimeToClose(self, evt):
        '''Event handler for the button click.'''
        print "See ya later!"
        self._ipc.close()
        self.Close()
        
    def OnONButton(self, evt):
        '''Event handler for the button click.'''
        print "IPC on"
        self._ipc.powerOn()
        self.on_btn.Disable()
        self.off_btn.Enable()
        self.panel.SetBackgroundColour(wx.GREEN)
        self.panel.Refresh()

    def OnOFFButton(self, evt):
        '''Event handler for the button click.'''
        print "IPC off"
        self._ipc.powerOff()
        self.off_btn.Disable()
        self.on_btn.Enable()
        self.panel.SetBackgroundColour(wx.RED)
        self.panel.Refresh()

    def OnAbout(self, evt):
        ''' Respond to the "About" menu command.
        '''
        dialog = wx.Dialog(self, -1, "About Power On Off" ,
                            style=wx.DIALOG_MODAL | wx.STAY_ON_TOP)
        dialog.SetBackgroundColour(wx.WHITE)

        panel = wx.Panel(dialog, -1)
        panel.SetBackgroundColour(wx.WHITE)

        panelSizer = wx.BoxSizer(wx.VERTICAL)

        boldFont = wx.Font(panel.GetFont().GetPointSize(),
                          panel.GetFont().GetFamily(),
                          wx.NORMAL, wx.BOLD)

        logo = wx.StaticBitmap(panel, -1, wx.Bitmap("resources/acc.png",
                                                 wx.BITMAP_TYPE_PNG))

        lab1 = wx.StaticText(panel, -1, "Power On Off")
        lab1.SetFont(wx.Font(36, boldFont.GetFamily(), wx.ITALIC, wx.BOLD))
        lab1.SetSize(lab1.GetBestSize())

        imageSizer = wx.BoxSizer(wx.HORIZONTAL)
        imageSizer.Add(logo, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)
        imageSizer.Add(lab1, 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)

        lab2 = wx.StaticText(panel, -1, "A simple program to control IPC device")
        lab2.SetFont(boldFont)
        lab2.SetSize(lab2.GetBestSize())

        lab3 = wx.StaticText(panel, -1, "Power On Off is completely free " + \
                                       "software; please")
        lab3.SetFont(boldFont)
        lab3.SetSize(lab3.GetBestSize())

        lab4 = wx.StaticText(panel, -1, "feel free to adapt or use this " + \
                                       "in any way you like.")
        lab4.SetFont(boldFont)
        lab4.SetSize(lab4.GetBestSize())

        lab5 = wx.StaticText(panel, -1, __info__)
                             #"Author: Ilan Finci " + \
                             #"(Ilan@Finci.org)\n")

        lab5.SetFont(boldFont)
        lab5.SetSize(lab5.GetBestSize())

        btnOK = wx.Button(panel, wx.ID_OK, "OK")

        panelSizer.Add(imageSizer, 0, wx.ALIGN_CENTRE)
        panelSizer.Add((10, 10)) # Spacer.
        panelSizer.Add(lab2, 0, wx.ALIGN_CENTRE)
        panelSizer.Add((10, 10)) # Spacer.
        panelSizer.Add(lab3, 0, wx.ALIGN_CENTRE)
        panelSizer.Add(lab4, 0, wx.ALIGN_CENTRE)
        panelSizer.Add((10, 10)) # Spacer.
        panelSizer.Add(lab5, 0, wx.ALIGN_CENTRE)
        panelSizer.Add((10, 10)) # Spacer.
        panelSizer.Add(btnOK, 0, wx.ALL | wx.ALIGN_CENTRE, 5)

        panel.SetAutoLayout(True)
        panel.SetSizer(panelSizer)
        panelSizer.Fit(panel)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(panel, 0, wx.ALL, 10)

        dialog.SetAutoLayout(True)
        dialog.SetSizer(topSizer)
        topSizer.Fit(dialog)

        dialog.Centre()

        btn = dialog.ShowModal()
        dialog.Destroy()
        
        
class PooApp(wx.App):
    def OnInit(self):
        frame = PooFrame(None, "Power On Off")
        self.SetTopWindow(frame)

        frame.Show(True)
        return True



def main():
    ''' Start up the application.
    '''
    global _app

    # Create and start the pySketch application.

    _app = PooApp(0)
    _app.MainLoop()


if __name__ == "__main__":
    main()
