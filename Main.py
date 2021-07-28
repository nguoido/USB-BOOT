#!/usr/bin/env python

import wx
import wx.adv
import wx.lib.inspection
import wx.lib.mixins.inspection

import sys
import os

# stuff for debugging
print("Python version:", sys.version)
print("wxPython version:", wx.version())

# ---------------------------------------------------------------------------
class UsbBootFlasher(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(300, 450),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.__init_ui()

    def __init_ui(self):
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.VERTICAL)

        hbox.AddSpacer(10)
        port_label = wx.StaticText(panel, label="Device")
        hbox.Add(port_label, 0, wx.ALL, 3)

        serial_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.choice = wx.Choice(panel, choices=["usb1", "usb2", "usb3"])
        self.choice.Bind(wx.EVT_CHOICE, self.__on_select_port)
        serial_boxsizer.Add(self.choice, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        hbox.Add(serial_boxsizer, 0, wx.EXPAND, 0)

        # ---------------------------------------------------------------------------
        hbox.AddSpacer(10)
        capacity_label = wx.StaticText(panel, label="Capacity")
        hbox.Add(capacity_label, 0, wx.ALL, 3)

        capacity_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.choice = wx.Choice(panel, choices=["4G", "8GB", "16G"])
        self.choice.Bind(wx.EVT_CHOICE, self.__on_select_port)
        capacity_boxsizer.Add(self.choice, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        hbox.Add(capacity_boxsizer, 0, wx.EXPAND, 0)

        # ---------------------------------------------------------------------------
        hbox.AddSpacer(10)
        fs_label = wx.StaticText(panel, label="File System")
        hbox.Add(fs_label, 0, wx.ALL, 3)

        fs_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.choice = wx.Choice(panel, choices=["FAT", "NTFS", "EXT4"])
        self.choice.Bind(wx.EVT_CHOICE, self.__on_select_port)
        fs_boxsizer.Add(self.choice, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        hbox.Add(fs_boxsizer, 0, wx.EXPAND, 0)
        panel.SetSizer(hbox)

        # ---------------------------------------------------------------------------
        hbox.AddSpacer(10)
        cs_label = wx.StaticText(panel, label="Cluster size")
        hbox.Add(cs_label, 0, wx.ALL, 3)

        cs_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.choice = wx.Choice(panel, choices=["4029 bytes", "512 bytes"])
        self.choice.Bind(wx.EVT_CHOICE, self.__on_select_port)
        cs_boxsizer.Add(self.choice, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        hbox.Add(cs_boxsizer, 0, wx.EXPAND, 0)
        panel.SetSizer(hbox)

        # ---------------------------------------------------------------------------
        hbox.AddSpacer(10)
        nvl_label = wx.StaticText(panel, label="New Volume Label")
        hbox.Add(nvl_label, 0, wx.ALL, 3)

        self.console_ctrl =  wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.console_ctrl.SetValue("4029 bytes")

        hbox.Add(self.console_ctrl, 0, wx.EXPAND)

        # ---------------------------------------------------------------------------
        hbox.AddSpacer(10)
        f_options = wx.StaticText(panel, label="Format options:")
        hbox.Add(f_options, 0, wx.ALL, 3)

        format_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        format_boxsizer.AddSpacer(10)
        format_boxsizer.Add(wx.RadioButton(panel, name="Quick format", label="Quick format", style=wx.RB_GROUP))
        hbox.Add(format_boxsizer, 0, wx.EXPAND, 3)

        # ---------------------------------------------------------------------------
        hbox.AddSpacer(30)
        bt_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        bt_boxsizer.AddStretchSpacer(0)

        self.__btFlash = wx.Button(panel, label="Flash")
        self.__btFlash.Bind(wx.EVT_BUTTON, self.__on_clicked)
        bt_boxsizer.Add(self.__btFlash, 0, wx.ALL, 3)

        self.__btClose = wx.Button(panel, label="Close")
        self.__btClose.Bind(wx.EVT_BUTTON, self.__on_clicked)
        bt_boxsizer.Add(self.__btClose, 0, wx.ALL, 3)

        hbox.Add(bt_boxsizer, 0, wx.ALIGN_RIGHT, 0)
        # ---------------------------------------------------------------------------

        panel.SetSizer(hbox)

    def __on_select_port(self, event):
        choice = event.GetEventObject()
        out = choice.GetString(choice.GetSelection())
        print(out)

    def __on_clicked(self, event):
        print("abc")

# ---------------------------------------------------------------------------
class MySplashScreen(wx.adv.SplashScreen):
    def __init__(self):
        wx.adv.SplashScreen.__init__(self, images.Splash.GetBitmap(),
                                     wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 2500, None, -1)
        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.__fc = wx.CallLater(2000, self._show_main)

    def _on_close(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.__fc.IsRunning():
            self.__fc.Stop()
            self._show_main()

    def _show_main(self):
        frame = UsbBootFlasher(None, "USB BOOT")
        frame.Show()
        if self.__fc.IsRunning():
            self.Raise()

# ----------------------------------------------------------------------------
class App(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):

        import images as i
        global images
        images = i

        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName("USB BOOT")

        # Create and show the splash screen.  It will then create and
        # show the main frame when it is time to do so.  Normally when
        # using a SplashScreen you would create it, show it and then
        # continue on with the application's initialization, finally
        # creating and showing the main application window(s).  In
        # this case we have nothing else to do so we'll delay showing
        # the main frame until later (see ShowMain above) so the users
        # can see the SplashScreen effect.
        splash = MySplashScreen()
        splash.Show()

        return True


# ---------------------------------------------------------------------------
def main():
    app = App(False)
    app.MainLoop()
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    __name__ = 'Main'
    main()

