import tkinter as tk
from tkinter import ttk

# a special popup window class that helps with user-input
class popupWindow(tk.Tk):
    __slots__ = ['__message', '__windowName']

    def __init__(self, message: str):
        self.__message = message
        self.__windowName = 'Alert'
        
        # since the class implements tk.Tk, its parent __init__ method must be called
        super().__init__()
        self.title(self.__windowName)
        self.resizable(False, False)   

    def display_error(self):
        ttk.Label(self, text = 'ERROR: ' + self.__message).pack(padx = 10, pady = 10)
        ttk.Button(self, text = 'Ok', command = self.destroy).pack(padx = 10, pady = 10, anchor = tk.S)
        # since the width of the window will vary depending on the message, this method is used since it displays windows in the middle of the screen regardless of size
        # it must be called AFTER the label is created
        self.eval('tk::PlaceWindow . center')

        self.mainloop()

    def display_popup(self):
        ttk.Label(self, text = self.__message).pack(padx = 10, pady = 10)
        ttk.Button(self, text = 'Ok', command = self.destroy).pack(padx = 10, pady = 10, anchor = tk.S)
        self.eval('tk::PlaceWindow . center')

        self.mainloop()