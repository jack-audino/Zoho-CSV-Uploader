import token_generator, popup_window, csv_parser, insert_lead, re, tkinter as tk
from tkinter import Frame, Toplevel, ttk, filedialog

# The main window that opens on boot
class Gui(tk.Tk):
    __slots__ = ['__windowName', '__windowWidth', '__windowHeight']

    def __init__(self, windowName: str, windowWidth: int, windowHeight: int):
        self.__windowName = windowName
        self.__windowWidth = windowWidth
        self.__windowHeight = windowHeight
        
        super().__init__()

        self.title(self.__windowName)

        xPos = (self.winfo_screenwidth() / 2) - (self.__windowWidth / 2)
        yPos = (self.winfo_screenheight() / 2) - (self.__windowHeight / 2)
        
        self.geometry(str(self.__windowWidth) + 'x' + str(self.__windowHeight) + '+' + str(int(xPos)) + '+' + str(int(yPos)))
        self.resizable(False, False)

    def display_items(self):
        # the 'change directory', 'open devWindow', and 'select home directory' buttons should be defined above the upload button so that any variables changed are saved before uploading

        # Header Label
        factory(ttk.Label, self, True, 'Zoho CSV Uploader', fontParams = ('DejaVu Sans', '30', 'bold'), xFrac = 0.5, yFrac = 0.1, anchorPos = tk.CENTER)

        # 'Change Home Directory' Button
        factory(ttk.Button, self, True, 'Select a home directory', givenCommand = self.change_dir, xFrac = 0.5, yFrac = 0.6, anchorPos = tk.CENTER)

        # 'Open Developer Window' Button
        # in order to pass parameters into button commands, 'lambda:' must be written before calling it, otherwise it will just run the method upon being set equal to the givenCommand
        factory(ttk.Button, self, True, 'Open the Developer Window', givenCommand = lambda: devWindow(self),  xFrac = 0.5, yFrac = 0.85, anchorPos = tk.CENTER)

        # 'Upload File' Button
        factory(ttk.Button, self, True, 'Select a file to upload to Zoho', givenCommand = self.file_dialog, xFrac = 0.5, yFrac = 0.5, anchorPos = tk.CENTER)
        self.mainloop()

    # method called when the 'Upload File' button is pressed
    def file_dialog(self):
        # read the config file to access the most current home directory, if there is none, then just start at 'C:/'
        homeDir = token_generator.read_config('HOME_DIRECTORY')
        if homeDir is None:
            csvFilepath = filedialog.askopenfile(title = 'Select a csv file', initialdir = '/', filetypes = (('csv files', '*csv'), ('All files', '*.*')))
        else:
            csvFilepath = filedialog.askopenfile(title = 'Select a csv file', initialdir = homeDir, filetypes = (('csv files', '*csv'), ('All files', '*.*')))
            # by setting csvFilePath equal to the askopenfile prompt, it will allow the file path returned to be stored in a variable for later use

        if csvFilepath is not None:
            if type(csvFilepath) == str:
                parser = csv_parser.CSVParser(csvFilepath)
            else:
                parser = csv_parser.CSVParser(csvFilepath.name) # .name returns the filepath as a string instead of an object
            try:
                parser.parse()

            except Exception:
                error = popup_window.popupWindow('Parsing Error.')
                error.display_error()

            parsed = parser.get_parsed()
            response = insert_lead.send_parsed(parsed)

            if response is not None:
                # if 'SUCCESS is not in the response data sent from the webpage, then display the error
                if 'SUCCESS' not in response:
                    error = popup_window.popupWindow(response)
                    error.display_error()

                elif 'SUCCESS' in response:
                    popup = popup_window.popupWindow('Data sent successfully.')
                    popup.display_popup()

    # simple method to change the home directory, called by the 'change home directory' button
    def change_dir(self):
        initDir = filedialog.askdirectory(title = 'Select a home directory', initialdir = '/')
        token_generator.write_to_config('HOME_DIRECTORY = ' + initDir, 'HOME_DIRECTORY')

# create a new class for the devWindow so it can be easily called above, without errors
class devWindow(Toplevel):
    __slots__ = ['__windowName', '__windowWidth', '__windowHeight']

    def __init__(self, master = None):
        self.__windowName = 'Developer Window'
        self.__windowWidth = 620
        self.__windowHeight = 260

        # master is the parent window
        super().__init__(master = master)

        self.title(self.__windowName)

        xPos = (self.winfo_screenwidth() / 2) - (self.__windowWidth / 2)
        yPos = (self.winfo_screenheight() / 2) - (self.__windowHeight / 2)

        self.geometry(str(self.__windowWidth) + 'x' + str(self.__windowHeight) + '+' + str(int(xPos)) + '+' + str(int(yPos)))
        self.resizable(False, False)

        # although it's messy code, display_items() has to be called in the init of devWindow since it's created through a button, so it can't be defined then have its display_items() called, since only one method can be called on a button press
        self.display_items()

    def display_items(self):
        # Label for the Edit Config Button and the Button itself
        factory(ttk.Label, self, True, 'Edit the configuration files:', xFrac = 0.2, yFrac = 0.2, anchorPos = tk.CENTER)
        factory(ttk.Button, self, True, 'Open Config Window', givenCommand = lambda: configWindow(self), xFrac = 0.2, yFrac = 0.3, anchorPos = tk.CENTER)

        # Use Grant Token Label, Disclaimer, and the Button itself
        factory(ttk.Label, self, True, 'Use the current Grant Token:', xFrac = 0.5, yFrac = 0.2, anchorPos = tk.CENTER)
        factory(ttk.Label, self, True, '(This will change the Refresh\nand Access Tokens,\nand Grant Tokens can only be used once.)', fontParams = ('DejaVu Sans', '7'), xFrac = 0.5, yFrac = 0.425, anchorPos = tk.CENTER, justifyPos = tk.CENTER)
        factory(ttk.Button, self, True, 'Use Grant Token', givenCommand = token_generator.use_grant_token, xFrac = 0.5, yFrac = 0.3, anchorPos = tk.CENTER)

        # Revoke Refresh Token Label, Disclaimer, and the Button itself
        factory(ttk.Label, self, True, 'Revoke the current Refresh Token\nand Refreshed Access Token:', xFrac = 0.8, yFrac = 0.2, anchorPos = tk.CENTER, justifyPos = tk.CENTER)
        factory(ttk.Label, self, True, '(This will delete the Refresh\nToken and Refreshed Access Token\nfrom the config file, and a\nnew one will need to be generated\n through a new Grant Token.)', fontParams = ('DejaVu Sans', '7'), xFrac = 0.8, yFrac = 0.475, anchorPos = tk.CENTER, justifyPos = tk.CENTER)
        factory(ttk.Button, self, True, 'Revoke', givenCommand = token_generator.revoke_refresh_token, xFrac = 0.8, yFrac = 0.3, anchorPos = tk.CENTER)

        # Wipe Config Label, Disclaimer, and the Button itself
        factory(ttk.Label, self, True, 'Wipe the current config:', xFrac = 0.5, yFrac = 0.65, anchorPos = tk.CENTER)
        factory(ttk.Label, self, True, '(This will delete all tokens, the saved Home Directory,\nthe Client ID, Client Secret, and new tokens will need to\nbe generated through a new Grant Token, and the Client ID\nand Client Secret will have to be re-entered.)', fontParams = ('DejaVu Sans', '7'), xFrac = 0.5, yFrac = 0.9, anchorPos = tk.CENTER, justifyPos = tk.CENTER)
        factory(ttk.Button, self, True, 'Wipe Config', givenCommand = token_generator.wipe_config, xFrac = 0.5, yFrac = 0.75, anchorPos = tk.CENTER)

        # self.mainloop() doesn't need to be called for child windows

# create a new class for the configWindow so it can be easily called above, without errors
class configWindow(Toplevel):
    __slots__ = ['__windowName', '__windowWidth', '__windowHeight']

    def __init__(self, master = None):
        self.__windowName = 'Config Window'
        self.__windowWidth = 675
        self.__windowHeight = 550

        super().__init__(master = master)

        self.title(self.__windowName)

        # in order to make the grid appear in the middle of the window, a frame must be added
        # since there are two grids with their own sizes, each should belong to its own frame
        topFrame = Frame(self)
        bottomFrame = Frame(self)

        xPos = (self.winfo_screenwidth() / 2) - (self.__windowWidth / 2)
        yPos = (self.winfo_screenheight() / 2) - (self.__windowHeight / 2)

        self.geometry(str(self.__windowWidth) + 'x' + str(self.__windowHeight) + '+' + str(int(xPos)) + '+' + str(int(yPos)))
        self.resizable(False, False)

        self.display_items(topFrame, bottomFrame)

    def display_items(self, tFrame: Frame, bFrame: Frame):
        accessTokenFromGrantStr = token_generator.read_config('ACCESS_TOKEN')
        accessTokenFromRefreshStr = token_generator.read_config('REFRESHED_ACCESS_TOKEN')
        refreshTokenStr = token_generator.read_config('REFRESH_TOKEN')
        homeDir = token_generator.read_config('HOME_DIRECTORY')

        # everything below has to be added to a specific frame, and not self (i.e. the window) since there are two different frames in the inside of it

        # Label for the current Grant Token, the Grant Token itself, the Grant Token description, and the prompt to the user to enter a new Grant Token
        self.display_entry(tFrame, token_generator.read_config('GRANT_TOKEN'), 'Current Grant Token:', 
        '(This is generated by putting the scope \"aaaserver.profile.ALL,\nZohoCRM.modules.leads.CREATE\" into the API console.)', 'Enter new Grant Token', 0, 0, 'GRANT_TOKEN')

        # Spacer cell
        factory(ttk.Label, tFrame, False, '', rowNum = 4, colNum = 0)

        # Label for the current Client ID, the Client ID itself, and the prompt to the user to enter a new Client ID
        self.display_entry(tFrame, token_generator.read_config('CLIENT_ID'), 'Current Client ID:', '(This was generated when a self-client was created using the API Console.)',
        'Enter new Client ID:', 5, 0, 'CLIENT_ID')

        # Spacer cell
        factory(ttk.Label, tFrame, False, '', rowNum = 9, colNum = 0)

        # Label for the current Client Secret, the Client Secret itself, and the prompt to the user to enter a new Client Secret
        self.display_entry(tFrame, token_generator.read_config('CLIENT_SECRET'), 'Current Client Secret:', '(This was generated when a self-client was created using the API Console.)',
        'Enter new Client Secret:', 10, 0, 'CLIENT_SECRET')
        
        tFrame.grid()
        tFrame.place(x = 10, y = 10)

        # The Label for the Grant-Gen'd Access Token, the Grant-Gen'd Access Token itself, and its description
        self.display_token(bFrame, 'Grant-Generated Access Token:', accessTokenFromGrantStr, '(This was generated by sending the Grant Token to the server.)', 0, 0)

        # Spacer cell
        factory(ttk.Label, bFrame, False, '', rowNum = 3, colNum = 0)

        # The Label for the Grant-Gen'd Refresh Token, the Grant-Gen'd Refresh Token itself, and its description
        self.display_token(bFrame, 'Grant-Generated Refresh Token:', refreshTokenStr, '(This was generated by sending the Grant Token to the server.)', 4, 0)

        # Spacer cell
        factory(ttk.Label, bFrame, False, '', rowNum = 6, colNum = 0)

        # The Label for the Refresh-Gen'd Access Token, the Refresh-Gen'd Access Token itself, and its description
        self.display_token(bFrame, 'Refresh-Generated Access Token:', accessTokenFromRefreshStr, '(This was generated by sending the Refresh Token (above) to the server.)', 7, 0)

        # Spacer cell
        factory(ttk.Label, bFrame, False, '', rowNum = 10, colNum = 0)

        self.display_token(bFrame, 'Home Directory:', homeDir, '', 11, 0)

        bFrame.place(x = 10, y = 340)
        
    # factory for displaying tokens, since they all have the same formatting
    def display_token(self, frame: Frame = None, title: str = None, token: str = None, description: str = None, startingRow: int = None, startingCol: int = None):
        # Title Label
        factory(ttk.Label, frame, False, title, fontParams = ('DejaVu Sans', '10', 'underline'), rowNum = startingRow, colNum = startingCol, stickyPos = 'w')

        # Actual Token Label (1 col to the right, on the same row)
        if token is None:
            factory(ttk.Label, frame, False, 'None', rowNum = startingRow, colNum = startingCol + 1, stickyPos = 'w')
        else:
            factory(ttk.Label, frame, False, token, rowNum = startingRow, colNum = startingCol + 1, stickyPos = 'w')

        # Description Label (1 col to the right, one row down)
        factory(ttk.Label, frame, False, description, rowNum = startingRow + 1, colNum = startingCol + 1, stickyPos = 'w')

    # factory for displaying entries, since they all have the same formatting
    def display_entry(self, frame: Frame = None, token: str = None, currentTokenLabel: str = None, description: str = None, enterStatement: str = None,
                        startingRow: int = None, startingCol: int = None, tokenType: str = None):
        factory(ttk.Label, frame, False, currentTokenLabel, fontParams = ('DejaVu Sans', '10', 'underline'), rowNum = startingRow, colNum = startingCol, stickyPos = 'w')

        if token is not None:
            tokenLabel = factory(ttk.Label, frame, False, token, rowNum = startingRow, colNum = startingCol + 1, stickyPos = 'w') 
        else:
            tokenLabel = factory(ttk.Label, frame, False, 'None', rowNum = startingRow, colNum = startingCol + 1, stickyPos = 'w')

        factory(ttk.Label, frame, False, description, rowNum = startingRow + 3, colNum = startingCol + 1, stickyPos = 'w')
        factory(ttk.Label, frame, False, enterStatement, fontParams = ('DejaVu Sans', '10', 'underline'), rowNum = startingRow + 2, colNum = startingCol, stickyPos = 'w')

        # The entry widget and its enter button that will take a new Grant Token and will save it upon hitting the enter button or key, and will update the label as well
        newTokenEntry = factory(tk.Entry, frame, False, entryWidth = 50, rowNum = startingRow + 1, colNum = startingCol + 1, stickyPos = 'w')
        # since the user may press enter while inputting a value into a textbox, it must be rebound to capture the data from the grantTokenInput textbox
        newTokenEntry.bind('<Return>', lambda event: self.use_input(tokenLabel, newTokenEntry, tokenType))
        newTokenEntry.bind('<KP_Enter>', lambda event: self.use_input(tokenLabel, newTokenEntry, tokenType))
        factory(ttk.Button, frame, False, 'Enter', givenCommand = lambda: self.use_input(tokenLabel, newTokenEntry, tokenType), rowNum = startingRow + 2, colNum = startingCol + 1, stickyPos = 'w')

    # to make checking entry values simpler (i.e. new grant tokens, client IDs and client Secrets)
    def use_input(self, labelVar: ttk.Label, entryVar: tk.Entry, itemName: str):
        newToken = entryVar.get()

        # if the input is completely empty, just wait for the next time input is given
        if len(newToken) == 0:
            entryVar.delete(0, tk.END)
            pass

        # if there's no whitespace, then add the new token
        elif re.search(r'^\S+$', newToken):
            token_generator.write_to_config(itemName + ' = ' + newToken, itemName)
            labelVar.config(text = newToken)
            entryVar.delete(0, tk.END)
            
        # if there's ONLY whitespace, don't prompt the user and just delete it
        elif re.search(r'^\s+$', newToken):
            entryVar.delete(0, tk.END)
            pass

        # if there's whitespace, prompt the user, but don't delete their input
        elif re.search(r'\s', newToken):
            error = popup_window.popupWindow('No whitespace, please.')
            error.display_error()

# to make the code much more concise, a global factory method was added to make labels, entries, text, etc
def factory(widget: ttk.Widget, master, usingPlace: bool, textInput: str = None, rowNum: int = None, colNum: int = None,
            stickyPos: str = None, xFrac: float = None, yFrac: float = None, anchorPos = None, givenCommand = None, 
            fontParams: tuple = (), entryWidth: str = None, justifyPos = None):

    if usingPlace == True:
        if widget.__name__ == 'Label':
            label = ttk.Label(master = master, text = textInput, font = fontParams, justify = justifyPos)
            label.place(relx = xFrac, rely = yFrac, anchor = anchorPos)
            return label

        elif widget.__name__ == 'Button':
            button = ttk.Button(master = master, text = textInput, command = givenCommand)
            button.place(relx = xFrac, rely = yFrac, anchor = anchorPos)
            return button

        elif widget.__name__ == 'Entry':
            entry = tk.Entry(master = master, width = entryWidth)
            entry.place(relx = xFrac, rely = yFrac, anchor = anchorPos)
            return entry
        
    else:
        if widget.__name__ == 'Label':
            label = ttk.Label(master = master, text = textInput, font = fontParams)
            label.grid(row = rowNum, column = colNum, sticky = stickyPos)
            return label

        elif widget.__name__ == 'Button':
            button = ttk.Button(master = master, text = textInput, command = givenCommand)
            button.grid(row = rowNum, column = colNum, sticky = stickyPos)
            return button

        elif widget.__name__ == 'Entry':
            entry = tk.Entry(master = master, width = entryWidth)
            entry.grid(row = rowNum, column = colNum, sticky = stickyPos)
            return entry