import gui

def main():
    # most of the code is executed in the gui.py since tkinter uses loops and breaking out of them would close the windows
    mainWindow = gui.Gui('Zoho CSV Uploader', 500, 400)
    mainWindow.display_items()
    
main()