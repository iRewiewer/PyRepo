import customtkinter as ctk
import pyautogui

from tkinter import CENTER
from random import randint
from pynput.mouse import Button, Controller
from datetime import datetime
from threading import Thread
from pathlib import Path
from time import sleep
from os import listdir

mouse = Controller()
threadIsRunning = True
macros = []

def recordMacro(recordMacroButton, loadMacroComboBox):
    global threadIsRunning

    if recordMacroButton.cget("text") == "Record Macro":
        threadIsRunning = True
        thread = Thread(target = _recordMacro, args = (loadMacroComboBox, ))
        thread.start()
        recordMacroButton.configure(text = "Stop")
    else:
        threadIsRunning = False
        recordMacroButton.configure(text = "Record Macro")

def _recordMacro(loadMacroComboBox):
    global threadIsRunning
    global mouse

    fileName = datetime.now().strftime("%d-%m-%Y - %H;%M;%S")
    fileContents = ""

    while threadIsRunning:
        pos = pyautogui.position()
        print(pos)
        fileContents += f"({pos.x},{pos.y})\n"
        sleep(0.001)

    dialog = ctk.CTkInputDialog(text = "Input name of macro", title = "Pycro")
    dialogInput = dialog.get_input()

    try:
        file = open(Path().resolve()/f"{dialogInput}.pycro", 'w')
        macros.append(f"{dialogInput}")
    except:
        file = open(Path().resolve()/f"{fileName}.pycro", 'w')
        macros.append(f"{fileName}")

    loadMacroComboBox.configure(values = macros)
    loadMacroComboBox.configure(state = "normal")
    loadMacroComboBox.set(macros[0])

    file.write(fileContents)
    file.close()

def loadMacro(loadMacroButton, loadMacroComboBox):
    try:
        file = open(Path().resolve()/f"{loadMacroComboBox.get()}.pycro")
    except:
        warningWindow = ctk.CTkToplevel()
        warningWindow.geometry("200x100")
        warningWindow.title("Pycro")
        label = ctk.CTkLabel(warningWindow, text = "Error loading macro file.")
        label.pack(side = "top", fill = "both", expand = True)
        return

    loadMacroButton.configure(text = "Running...")
    thread = Thread(target = _loadMacro, args = (file.read().split("\n"), loadMacroButton,))
    thread.start()

def _loadMacro(contents, loadMacroButton):
    for i in contents:
        print(i)

    loadMacroButton.configure(text = "Load Macro")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App settings
        self.geometry(f"{300}x{150}")
        self.appearance_mode = "dark" # Modes: system (default), light, dark
        self.default_color_theme = "blue" # Themes: blue (default), dark-blue, green
        self.title("Pycro")
        self.start()

    def start(self):
        # Get all macros in parent folder
        macros = [file.split(".")[0] for file in listdir(Path().resolve()) if file.split('.')[-1] == "pycro"]
        loadMacroComboBox = ctk.CTkComboBox(master = self, values = macros)
        loadMacroComboBox.place(width = 250, relx = 0.5, rely = 0.3, anchor = CENTER)

        # Disable combo box if there are no macros
        if len(macros) == 0:
            loadMacroComboBox.set(" ")
            loadMacroComboBox.configure(state = "disabled")

        recordMacroButton = ctk.CTkButton(master = self, text = "Record Macro", command = lambda: recordMacro(recordMacroButton, loadMacroComboBox))
        recordMacroButton.place(width = 100, relx = 0.25, rely = 0.7, anchor = CENTER)

        loadMacroButton = ctk.CTkButton(master = self, text = "Load Macro", command = lambda: loadMacro(loadMacroButton, loadMacroComboBox))
        loadMacroButton.place(width = 100, relx = 0.75, rely = 0.7, anchor = CENTER)

app = App()
app.mainloop()