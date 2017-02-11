import wx
import wx.lib.agw.flatnotebook as fnb
import wx.stc as stc


class DirTree(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour(wx.WHITE)
        self.dir = wx.GenericDirCtrl(self, wx.ID_ANY, dir='~/Desktop', style=wx.DIRCTRL_DIR_ONLY)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.dir, proportion=1, flag=wx.GROW)
        self.SetSizer(layout)

class TabPage(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.textCtrl = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.sizer.Add(self.textCtrl, wx.ID_ANY, wx.EXPAND)

        self.filename = ""
        self.directory = ""
        self.saved = False
        self.last_save = ""

class Right(fnb.FlatNotebook):

    def __init__(self, parent, id):

        fnb.FlatNotebook.__init__(self, parent, id,
                                  agwStyle=fnb.FNB_X_ON_TAB |
                                  fnb.FNB_NO_NAV_BUTTONS |
                                  fnb.FNB_NO_X_BUTTON)

        self.firstTabPage()

    def firstTabPage(self):
        name = "untitled"
        firstPanel = wx.Panel(self, wx.ID_ANY)

        text = stc.StyledTextCtrl(firstPanel, wx.ID_ANY)
        text.SetMarginType(1, stc.STC_MARGIN_NUMBER)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(text, proportion=1, flag=wx.GROW)
        firstPanel.SetSizer(layout)

        self.AddPage(firstPanel, name)

    def NewFileTab(self, event):
        name = "untitled"
        newPanel = wx.Panel(self, wx.ID_ANY)
        newPanel.SetFocus()

        self.text = stc.StyledTextCtrl(newPanel)
        self.text.SetMarginType(1, stc.STC_MARGIN_NUMBER)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.text, proportion=1, flag=wx.GROW)
        newPanel.SetSizer(layout)

        self.AddPage(newPanel, name, select=True)


class MainFrame(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))

        splitter = wx.SplitterWindow(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        splitter.SetMinimumPaneSize(50)

        leftPane = DirTree(splitter, wx.ID_ANY)
        rightPane = Right(splitter, wx.ID_ANY)
        splitter.SplitVertically(leftPane, rightPane)

        self.menubar = wx.MenuBar()
        self.filemenu = wx.Menu()

        self.newFile = self.filemenu.Append(wx.ID_ANY, '&New\tCtrl+N', "Create a New Tab")
        self.filemenu.AppendSeparator()

        self.menubar.Append(self.filemenu, "&File")
        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_MENU, rightPane.NewFileTab, self.newFile)


if __name__ == "__main__":
    app = wx.App(False)
    mainFrame = MainFrame(None, wx.ID_ANY, "Pynapple")
    icon = wx.EmptyIcon()
    iconImage = wx.Image('icon.png', wx.BITMAP_TYPE_PNG)
    icon.CopyFromBitmap(iconImage.ConvertToBitmap())
    mainFrame.SetIcon(icon)
    mainFrame.Show()
    app.MainLoop()