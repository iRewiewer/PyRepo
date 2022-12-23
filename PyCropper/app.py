from PIL import Image
from os import listdir, remove, mkdir, path
from shutil import rmtree
import wx

def cropp(left, top, right, bottom):
    if(not path.exists("./cropped")):
        mkdir(path.join("./" + "cropped"))

    for i in listdir():
        if i[-4:] == ".jpg" or i[-4:] == ".png":
            img = Image.open(i)
            croppedImg = img.crop((left, top, right, bottom))
            croppedImg.save("./cropped/" + i)

def removeOriginals():
    for i in listdir():
        if path.isfile(i) and (i[-4:] == ".jpg" or i[-4:] == ".jpg"):
            remove(i)

def removeCropped():
    rmtree("./cropped")

class Cropper(wx.App):
    def OnInit(self):
        self.frame = Frame(None, "v2.0", (352, 204), wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.CAPTION)

        return True

class Frame(wx.Frame):
    def __init__(self, parent, appVersion, size, style):
        super(Frame, self).__init__(parent = parent, title = "Cropper " + appVersion, size = size, style = style)

        ### GUI Elements ###

        self.panel = wx.Panel(self)

        self.title = wx.StaticText(self.panel, label = "Cropper v2.0", pos = (122, 10), size = (200, 20))
        font = wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.title.SetFont(font)

        self.left_label = wx.StaticText(self.panel, label = "Left:", pos = (30, 50), size = (22, 20))
        self.left_text  = wx.TextCtrl(self.panel, pos = (60, 50), size = (100, 20))

        self.top_label = wx.StaticText(self.panel, label = "Bottom:", pos = (10, 80), size = (45, 20))
        self.top_text  = wx.TextCtrl(self.panel, pos = (60, 80), size = (100, 20))

        self.right_label = wx.StaticText(self.panel, label = "Right:", pos = (182, 50), size = (30, 20))
        self.right_text  = wx.TextCtrl(self.panel, pos = (220, 50), size = (100, 20))

        self.bottom_label = wx.StaticText(self.panel, label = "Bottom:", pos = (170, 80), size = (50, 20))
        self.bottom_text  = wx.TextCtrl(self.panel, pos = (220, 80), size = (100, 20))

        self.author = wx.StaticText(self.panel, label = "by iRewiewer", pos = (205, 30), size = (80, 10))
        font = wx.Font(6, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.author.SetFont(font)



        ### Buttons ###

        self.rmCroppedBtn = wx.Button(self.panel, label = "Remove cropped", pos = (10, 120), size = (110, 35))
        self.rmCroppedBtn.Bind(wx.EVT_BUTTON, self.rmCropped)

        self.cropBtn = wx.Button(self.panel, label = "Crop!", pos = (137, 120), size = (60, 35))
        self.cropBtn.Bind(wx.EVT_BUTTON, self.cropFunc)

        self.rmOriginalsBtn = wx.Button(self.panel, label = "Remove originals", pos = (214, 120), size = (110, 35))
        self.rmOriginalsBtn.Bind(wx.EVT_BUTTON, self.rmOriginals)

        self.Show(True)

    def cropFunc(self, event):
        if len(self.left_text.GetValue()) == 0 or len(self.top_text.GetValue()) == 0 or len(self.right_text.GetValue()) == 0 or len(self.bottom_text.GetValue()) == 0:
            alertBox = wx.MessageDialog(self.panel, "Have you inputted the right values?", "Cropper - Crop images", wx.YES_NO)
            alertAnswer = alertBox.ShowModal()
            alertBox.Destroy()
            if alertAnswer == wx.ID_YES:
                if len(self.left_text.GetValue()) == 0: self.left_text.SetValue("237")
                if len(self.top_text.GetValue()) == 0: self.top_text.SetValue("95")
                if len(self.right_text.GetValue()) == 0: self.right_text.SetValue("1460")
                if len(self.bottom_text.GetValue()) == 0: self.bottom_text.SetValue("1013")

                try:
                    cropp(int(self.left_text.GetValue()), int(self.top_text.GetValue()), int(self.right_text.GetValue()), int(self.bottom_text.GetValue()))
                    alertBx = wx.MessageDialog(self.panel, "All images have been cropped successfully!", "Cropper - Crop images", wx.OK)
                    alertBx.ShowModal()
                    alertBx.Destroy()
                except:
                    alertBx = wx.MessageDialog(self.panel, "[Error 404] \nCropping files failed. \nPerhaps there aren't any files to crop?", "Cropper - Crop images", wx.ICON_EXCLAMATION)
                    alertBx.ShowModal()
                    alertBx.Destroy()
        else:
            alertBox = wx.MessageDialog(self.panel, "Are you sure you want to proceed?", "Cropper - Crop images", wx.YES_NO)
            alertAnswer = alertBox.ShowModal()
            alertBox.Destroy()
            if alertAnswer == wx.ID_YES:
                try:
                    cropp(int(self.left_text.GetValue()), int(self.top_text.GetValue()), int(self.right_text.GetValue()), int(self.bottom_text.GetValue()))
                    alertBx = wx.MessageDialog(self.panel, "Cropped files have been removed successfully!", "Cropper - Crop images", wx.OK)
                    alertBx.ShowModal()
                    alertBx.Destroy()
                except:
                    alertBx = wx.MessageDialog(self.panel, "[Error 404] \nCropping files failed. \nPerhaps there aren't any files to crop?", "Cropper - Crop images", wx.ICON_EXCLAMATION)
                    alertBx.ShowModal()
                    alertBx.Destroy()

    def rmCropped(self, event):
        alertBox = wx.MessageDialog(self.panel, "Are you sure you want to proceed?", "Cropper - Remove cropped", wx.YES_NO)
        alertAnswer = alertBox.ShowModal()
        alertBox.Destroy()
        if alertAnswer == wx.ID_YES:
            try:
                removeCropped()
                alertBx = wx.MessageDialog(self.panel, "Cropped files have been removed successfully!", "Cropper - Remove cropped", wx.OK)
                alertBx.ShowModal()
                alertBx.Destroy()
            except:
                alertBx = wx.MessageDialog(self.panel, "[Error 404] \nDeleting cropped files failed. \nPerhaps there aren't any?", "Cropper - Remove cropped", wx.ICON_EXCLAMATION)
                alertBx.ShowModal()
                alertBx.Destroy()

    def rmOriginals(self, event):
        alertBox = wx.MessageDialog(self.panel, "Are you sure you want to proceed?", "Cropper - Remove originals", wx.YES_NO)
        alertAnswer = alertBox.ShowModal()
        alertBox.Destroy()
        if alertAnswer == wx.ID_YES:
            try:
                removeOriginals()
                alertBx = wx.MessageDialog(self.panel, "Original files have been removed successfully!", "Cropper - Remove originals", wx.OK)
                alertBx.ShowModal()
                alertBx.Destroy()
            except:
                alertBx = wx.MessageDialog(self.panel, "[Error 404] \nDeleting originals files failed. \nPerhaps there aren't any?", "Cropper - Remove originals", wx.ICON_EXCLAMATION)
                alertBx.ShowModal()
                alertBx.Destroy()

Cropper().MainLoop()