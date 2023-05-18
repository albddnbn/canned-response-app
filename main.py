# Verified with Python 3.11.1, and module versions in requirements.txt
import tkinter as tk
# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
import tkinter.messagebox
from PIL import ImageTk, Image
import pyperclip
import os


# WINDOW DIMENSIONS (will be able to modify in the settings..eventually):
widths = {}
heights = {}
widths["main"] = 350
heights["main"] = 100
widths["view"] = 350
heights["view"] = 800
widths["add"] = 450
heights["add"] = 600


# Settings class that would take all 3 windows as argument?

class CannedFunctions:
    def __init__(self):
        pass
    # a 'normal' button in this case has a "#00467f" bg and white fg

    def style_normal_button(self, button):
        # set bg and fg
        button.background = "#00467f"
        button.foreground = "#ffffff"
        button.font = "Roboto 16 bold"
        # set the hovering actions
        self.set_hover_normal(button)

    def set_hover_normal(self, button):
        button.bind("<Enter>", func=lambda e: button.config(
            background="#ffffff", fg="#00467f"))
        button.bind("<Leave>", func=lambda e: button.config(
            background="#00467f", fg="#ffffff"))

    # erase text inside a Text widget when its clicked on, then unbind the erase function from the mouse click
    def erase_text(self, widget):
        widget.delete('1.0', tk.END)
        widget.bind("<Button-1>", func=lambda e: None)

    def change_window(self, tohide, toshow):
        tohide.withdraw()
        toshow.deiconify()

    def return_home(self, hide, show, windows):
        # hide both view / add windows:
        windows["view"].withdraw()
        windows["add"].withdraw()
        hide.withdraw()
        # tohide.withdraw()
        show.deiconify()

    def show_readme(self):
        # startfile opens the file with the system's default text editor (windows / linux / mac) according to stack overflow
        # https://stackoverflow.com/questions/43007196/python-open-a-textnotepad-document
        os.startfile("res\\readme.txt")

    def focus_next_widget(self, event):
        # if event.widget == title_entry:
        #     erase_text(content_entry)
        event.widget.tk_focusNext().focus()
        return ("break")

    def create_menu(self, window, windows_dict):
        # separate out the windows_dict:
        main_win = windows_dict["main"]
        add_win = windows_dict["add"]
        view_win = windows_dict["view"]
        settings_win = windows_dict["settings"]
        # create outer menubar
        menubar = tk.Menu(window)
        # create File cascade:
        filemenu = tk.Menu(menubar, tearoff=0)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Create new response",
                             command=lambda: add_win.change_window(window, add_win))
        filemenu.add_command(label="View stored responses",
                             command=lambda: view_win.view_stored_responses())

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=window.quit)

        menubar.add_cascade(label="File", menu=filemenu)

        # create Edit cascade
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(
            label="Settings", command=lambda: settings_win.deiconify())
        menubar.add_cascade(label="Edit", menu=editmenu)

        # create View cascade:
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="View scripts",
                             command=lambda: main_win.view_scripts())
        menubar.add_cascade(label="View", menu=viewmenu)

        # create Help cascade:

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About / Readme",
                             command=CannedFunctions.show_readme)
        helpmenu.add_separator()

        menubar.add_cascade(label="Help", menu=helpmenu)

        window.config(menu=menubar)


class Settings(tk.Toplevel, CannedFunctions):
    def __init__(self, windows):
        super().__init__()
        self.windows = windows
        self.main_win = self.windows["main"]
        self.view_win = self.windows["view"]
        self.add_win = self.windows["add"]

        self.geometry("400x300")
        self.title("Canned response app settings:")
        self.config(bg='#00a160')

        self.wm_attributes('-toolwindow', True)

        # title - 'Settings'
        settings_title = tk.Label(
            self, text="Settings: ", font="Roboto 14 bold", fg="#ffffff", bg="#00a160")

        settings_title.pack(side=tk.TOP, pady=(20, 15))

        # frame to contain all settings:
        settings_frame = tk.Frame(self, bg="#00a160")

        opacity_frame = tk.Frame(settings_frame, bg="#00a160")

        opacity_label = tk.Label(opacity_frame, text="Window opacity: ",
                                 font="Roboto 14 bold", fg="#ffffff", bg="#00a160")

        current_opacity = tk.IntVar()
        current_opacity.set(self.main_win.attributes("-alpha")*10)
        self.opacity_spinbox = tk.Spinbox(
            opacity_frame, from_=0, to=10, increment=1, textvariable=current_opacity, command=self.update_opacity)

        opacity_label.pack(side=tk.LEFT, padx=(5, 15))
        self.opacity_spinbox.pack(side=tk.RIGHT, padx=(5, 5))
        opacity_frame.pack(side=tk.TOP, padx=10, pady=5)

        settings_frame.pack()
        # on closing
        # self.protocol("WM_DELETE_WINDOW", self._on_closing)
        # hide window initially
        self.withdraw()

    def update_opacity(self):
        new_opacity = int(self.opacity_spinbox.get())/10

        self.windows["main"].attributes('-alpha', new_opacity)
        self.windows["view"].attributes('-alpha', new_opacity)

# The bottom frame which holds the Home button on the view/add response windows:


class BottomFrame(tk.Frame, CannedFunctions):
    def __init__(self, window, windows_dict):
        # separate out windows dict:
        main_win = windows_dict["main"]
        view_win = windows_dict["view"]
        add_win = windows_dict["add"]

        super().__init__(window, bg="#00a160")
        # home button photoimage
        self.home_photo = tk.PhotoImage(file="./img/home-tk.png")
        # btm_bars[key]["frame"] = tk.Frame(windows[key], bg="#00a160")
        self.home_button = tk.Button(self, image=self.home_photo, command=lambda: self.return_home(
            window, main_win, windows_dict))
        # self.home_button = tk.Button(self, image=self.home_photo, bg="#ffffff", command=lambda: self.return_home(view_win, main_win))
        self.home_button.image = self.home_photo
        self.pack(side=tk.BOTTOM, fill=tk.X)
        self.home_button.pack(side=tk.LEFT, padx=10, pady=10)
        # windows[key].withdraw()


class MainWindow(tk.Tk, CannedFunctions):
    def __init__(self, height, width, bg_color):
        """
        __init__ the home window - has two buttons on it: 'view' and 'add'

        _extended_summary_

        Args:
            height (int): height of main window
            width (int): width of main window
            bg_color (str): bg_color of main window in hex format
        """
        self.buttons = {
            "view": "",
            "add": ""
        }
        super().__init__()
        # set title / geometry:
        self.title("canned response app")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the top left point
        left_x = int(screen_width/4 - width / 2)
        top_y = int(screen_height/5 - height / 2)
        self.geometry(f'{width}x{height}+{left_x}+{top_y}')

        # Add a background color to the Main windows["main"]dow
        self.config(bg=bg_color)
        # set alpha to 0.5 initially (user can adjust through GUI settings)
        self.attributes('-alpha', 0.5)
        # create canvas for logo:
        logo_img = ImageTk.PhotoImage(Image.open("img\\logo.png"))

        # create the view and add buttons on main window:
        for button in ["view", "add"]:
            self.buttons[button] = tk.Button(
                self, font='Roboto 16 bold', bg="#00467f", fg="#ffffff", width=8)
            self.style_normal_button(self.buttons[button])
        self.buttons["view"]["text"] = "view"
        self.buttons["add"]["text"] = "add"

        self.buttons["view"].pack(side=tk.LEFT, padx=(35, 5), pady=0)
        self.buttons["add"].pack(side=tk.RIGHT, padx=(5, 35), pady=0)

    def view_scripts(self):
        # show a popup window with a clickable list of all the scripts files in the scripts directory
        # when a file is clicked, open it in the default text editor

        # get all files in scripts directory
        files = os.listdir("./scripts")
        # create a popup with listbox
        popup = tk.Toplevel(padx=10, pady=15)
        popup.title("View Scripts")
        popup.geometry("300x300")
        popup.config(bg="#00a160")
        # create a listbox
        listbox = tk.Listbox(popup, bg="#00a160",
                             fg="#ffffff", font="Roboto 14 bold")
        # give the popup some padding between it and listbox
        popup.rowconfigure(0, weight=1)
        popup.columnconfigure(0, weight=1)

        # add all files to listbox
        for file in files:
            listbox.insert(tk.END, file)
        # add a scrollbar
        scrollbar = tk.Scrollbar(popup)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # link scrollbar to listbox
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        # add a button to open the selected file
        open_button = tk.Button(
            popup, text="Open", command=lambda: self.open_script(listbox.get(tk.ACTIVE)))
        open_button.pack(side=tk.BOTTOM, pady=10)
        # pack the listbox
        listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # show the popup
        popup.mainloop()

    def open_script(self, file):
        # open the selected script file in the default text editor
        os.system(f"start ./scripts/{file}")

    def add_response(self):
        # show the add response window
        self.windows["add"].deiconify()
        self.windows["main"].withdraw()


class ViewWindow(tk.Toplevel, CannedFunctions):
    def __init__(self, win_master, win_height, win_width, win_title, add_win):
        """
        __init__ shows the 'view responses' part of the app, where you can view any responses that you've created or stored in the correct format.

        A row of buttons is generated for every response. Each row has a big dark blue button that copies the response to clipboard, a pencil/edit button that allows for editing of a response, and a trashcan icon that deletes a response and response file.

        Args:
            win_master (_type_): _description_
            win_height (int): _description_
            win_width (int): _description_
            win_title (str): _description_
            add_win (_type_): _description_
        """
        # main window
        self.win_master = win_master
        # add / create new response window
        self.add_window = add_win
        super().__init__(win_master)
        self.config(bg='#00a160')

        # set geometry of window
        self.geometry(f"{win_width}x{win_height}")

        # set title
        self.title = win_title

        # withdraw window initially
        self.withdraw()

        # create response buttons dictionary:
        self.response_buttons = {}

        # Label widget for 'title'
        self.view_title = tk.Label(
            self, text="View stored responses", bg="#00a160", font="Roboto 14 bold", fg="#ffffff")
        # textbox for user's name:
        self.name_txtbox = tk.Text(self, height=1, width=20)
        self.name_txtbox.insert('1.0', "Enter user's name")
        self.name_txtbox.bind(
            "<Button-1>", func=lambda e: self.erase_text(self.name_txtbox))

        # define the trash icon picture photo
        self.delete_img = tk.PhotoImage(file="./img/delete-tk.png")
        # define the edit icon
        self.edit_img = tk.PhotoImage(file="./img/edit-tk.png")

        # create large frame to hold all response buttons / etc.
        self.view_response_frame = tk.Frame(self)
        # pack view Window widgets
        self.view_title.pack(side=tk.TOP, padx=20, pady=(25, 10))
        self.name_txtbox.pack(side=tk.TOP, pady=(10, 10))
        self.view_response_frame.pack(
            side=tk.TOP, padx=10, pady=15, fill=tk.BOTH)
        self.attributes('-alpha', 0.5)
        self.wm_attributes('-topmost', True)

    def view_stored_responses(self):
        # print("view stored responses")
        # key list:
        keylist = ["frame", "padframe", "btn",
                   "edit", "delete", "view", "content"]

        # withdraw add window if its showing:
        self.add_window.withdraw()
        # need to CLEAR DICTS AND DELETE WIDGETS - response buttons
        for frame in self.view_response_frame.winfo_children():
            frame.destroy()

        # hide the main window, and show the view responses window
        self.win_master.withdraw()
        self.deiconify()
        # for every file in the responses directory
        for file in os.listdir("responses"):
            # if it is a response txt file (in the right format)
            if ("response-" in file) and (file.endswith(".txt")):
                with open(f"./responses/{file}", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    # first line of each txt file will be button title/text
                    # also chop of \n with [:-1]
                    title = lines[0][:-1]
                    print("viewing title: "+title)
                    self.response_buttons[title] = {}
                    for key in keylist:
                        if key == "content":
                            self.response_buttons[title][key] = []
                        else:
                            self.response_buttons[title][key] = ""
                    self.response_buttons[title]["frame"] = tk.Frame(
                        self.view_response_frame, bg="#00a160")
                    # padframe just adds some padding above each frame (tried to just add padding in when packing the frame, but background kept showing as white)
                    self.response_buttons[title]["padframe"] = tk.Frame(
                        self.response_buttons[title]["frame"], height=5, bg="#00a160")
                    self.response_buttons[title]["btn"] = tk.Button(self.response_buttons[title]['frame'], text=title, height=2, width=25,
                                                                    bg="#00467f", fg="#ffffff", command=lambda thistitle=title: self.copy_to_clipboard(thistitle), padx=1, pady=1)
                    self.response_buttons[title]["edit"] = tk.Button(
                        self.response_buttons[title]['frame'], image=self.edit_img,  bg="#00467f", fg="#ffffff", command=lambda thistitle=title: self.edit_response(thistitle))

                    # create the delete button:
                    self.response_buttons[title]["delete"] = tk.Button(self.response_buttons[title]['frame'], image=self.delete_img, command=lambda thistitle=title: self.delete_response(
                        thistitle), width=30, height=30,  bg="#00467f", fg="#ffffff")

                    for button in ["btn", "edit", "delete"]:
                        self.style_normal_button(
                            self.response_buttons[title][button])
                    self.response_buttons[title]["frame"]['background'] = "#00a160"
                    # load content into the 'content' key:
                    for line in lines[2:]:
                        self.response_buttons[title]['content'].append(line)

                    # pack frame:
                    self.response_buttons[title]['frame'].pack(
                        side=tk.TOP, fill=tk.BOTH)
                    self.response_buttons[title]["padframe"].pack(
                        side=tk.TOP, fill=tk.X)
                    self.response_buttons[title]['btn'].pack(
                        side=tk.LEFT, padx=(5, 5))
                    self.response_buttons[title]["edit"].pack(
                        side=tk.LEFT, padx=(5, 10))
                    self.response_buttons[title]["delete"].pack(
                        side=tk.LEFT, padx=5)

    # when edit button is clicked for a response - the create response window will open with the response's title / content inserted so it can be edited
    def edit_response(self, respon_title):
        """
        edit_response allows user to edit any of their stored responses.

        Edit a response by clicking any of the 'pencil' buttons next to any of the big dark blue buttons on the 'view' responses window.

        Args:
            respon_title (str): this is the title at the top of the edit response window, and also the name of the txt file that holds the response content
        """
        self.withdraw()

        # insert values into textboxes:
        self.add_window.title_entry.delete('1.0', 'end-1c')
        self.add_window.title_entry.insert('1.0', respon_title)
        self.add_window.content_entry.delete('1.0', 'end-1c')
        # create string of content:
        new_string = ""
        for line in self.response_buttons[respon_title]["content"]:
            new_string += line
        self.add_window.content_entry.insert('1.0', new_string)

        self.add_window.title_entry.unbind("<Button-1>")
        self.add_window.content_entry.unbind("<Button-1>")
        # show create response window
        self.add_window.deiconify()

    # when delete response button (trash can) is clicked
    def delete_response(self, resp_title):
        """
        delete_response lets user delete a response from the gui and the response txct file directory.

        Delete a response by clicking any of the trash can icons, next to any of the big dark blue buttons on the 'view' responses window.

        Args:
            resp_title (str): this is the title at the top of the edit response window, and also the name of the txt file that holds the response content
        """
        # all I need to do is delete the txt file, then call the update function and everything else will update itself based on the response-*.txt files in the directory
        os.remove(f"./responses/response-{resp_title}.txt")
        self.response_buttons[resp_title]
        self.update_view_responses()

    # updates the view responses window after deletion of a response
    def update_view_responses(self):
        """
        update_view_responses updates the dark blue response buttons on the 'view' window by recreating the group of buttons, <b>after</b> a response (And response file) has been deleted.

        So, the group of buttons will be reconstructed, and it won't have the button/response that was just deleted.
        """
        self.command = self.view_stored_responses
        self.win_master.after(500, self.view_stored_responses)

    def copy_to_clipboard(self, resp_title):
        """
        copy_to_clipboard copies the response text to the user's clipboard when a dark blue button is clicked.

        Whatever name is typed into the top textbox on the 'view' window will be inserted as the user's name into the responses. The name will take the place of the string '$owner' (without quotes) in response text.

        Args:
            resp_title (str): this is the title at the top of the edit response window, and also the name of the txt file that holds the response content
        """
        # get ticket owner's name from name_txtbox
        ticketowner = self.name_txtbox.get('1.0', 'end-1c')

        # copy ticket response to clipboard with owner's name inserted
        content = self.response_buttons[resp_title]["content"]
        new_string = ""
        for line in content:
            if "$owner" in line:
                line_w_name = line.replace("$owner", ticketowner)
            else:
                line_w_name = line
            new_string += f"{line_w_name}"
        pyperclip.copy(new_string)


class AddWindow(tk.Toplevel, CannedFunctions):
    def __init__(self, win_master, win_height, win_width, win_title):
        """
        __init__ window that allows a user to create a new response (this is also the edit response window).

        The user types in a title, and then types the body of the response, inserting '$owner' whereever they'd like the users' names to be inserted when the response is copied to the clipboard. A file is generated in the format: response-<title>.txt, and the response is saved in the file.

        Args:
            win_master (_type_): _description_
            win_height (_type_): _description_
            win_width (_type_): _description_
            win_title (_type_): _description_
        """
        # main window
        self.win_master = win_master
        # the view responses window
        # self.view_win = view_win
        super().__init__(win_master)

        self.geometry(f"{win_width}x{win_height}")
        self["bg"] = "#00a160"
        self.title = win_title
        # create frame to hold label and entry for title on the Add Response window:s
        self.title_frame = tk.Frame(self, bg="#00a160")
        self.title_frame.pack(side=tk.TOP, padx=5, pady=5)

        # label to go beside the title textbox
        self.title_label = tk.Label(
            self.title_frame, text="Response title: ", font="Roboto 14 bold", fg="#ffffff", bg="#00a160")
        self.title_label.pack(side=tk.LEFT, padx=(15, 5), pady=10)
        # textbox to enter ticket response title
        self.title_entry = tk.Text(self.title_frame, width=20, height=1)
        # insert this into the textbox initially
        self.title_entry.insert('1.0', "Ticket response title")
        # when user clicks on the textbox, it will auto-erase the initial text, and then release the click / erase binding (done in erase_text)
        self.title_entry.bind(
            "<Button-1>", func=lambda e: self.erase_text(self.title_entry))
        # bind function to title entry so when tab is pressed it will move cursor down to the content_entry (adds to efficiency/speed of use)
        self.title_entry.bind("<Tab>", self.focus_next_widget)
        # bigger textbox to hold the ticket response content
        self.content_entry = tk.Text(self, width=40, height=25)
        self.content_entry.insert('1.0', "Ticket response content")
        self.content_entry.bind(
            "<Button-1>", func=lambda e: self.erase_text(self.content_entry))
        # big button to go below the content textbox - click to create the response, i.e. the response-*.txt file
        self.create_resp_btn = tk.Button(self, text="Create response", width=20, command=lambda entries=[
                                         self.title_entry, self.content_entry]: self.create_response(entries[0], entries[1]))
        self.style_normal_button(self.create_resp_btn)

        self.create_resp_btn.pack(side=tk.BOTTOM, padx=25, pady=(10, 75))
        self.title_entry.pack(side=tk.RIGHT, padx=(5, 20), pady=15)

        self.content_entry.pack(side=tk.TOP, padx=20, pady=(5, 20))
        self.withdraw()

    def create_response(self, title, response_content):
        # since the widgets are transferred in as parameters, I need to take the value/text to get current text in them
        title = title.get(1.0, "end-1c")
        response_content = response_content.get(1.0, "end-1c")
        with open(f"./responses/response-{title}.txt", "w", encoding="utf-8") as txtfile:
            txtfile.write(f"{title}\n\n")
            txtfile.writelines(response_content)
        # notify user
        tkinter.messagebox.showinfo(
            'Ticket Response file created', f"[+] ./responses/response-{title}.txt created")
        self.erase_text(self.content_entry)
        self.erase_text(self.title_entry)


class TicketApplication(CannedFunctions):
    def __init__(self):
        """
        __init__ container class for the ticket application - holds all windows of the app in a dictionary (self.windows).
        """
        # 3 windows:
        self.windows = {
            # create root/main window
            "main": MainWindow(heights["main"], widths["main"], "#00a160"),
            "view": "",
            "add": "",
            "settings": ""
        }
        # create the view and add response windows
        self.windows["add"] = AddWindow(
            self.windows["main"], heights["view"], widths["view"], "View stored responses")
        self.windows["view"] = ViewWindow(
            self.windows["main"], heights["view"], widths["view"], "Create ticket response:", self.windows["add"])
        self.windows["settings"] = Settings(self.windows)
        # instantiate ? settings stuff
        self.settings = Settings(self.windows)
        logo_img = ImageTk.PhotoImage(Image.open(
            'img\\ticket-bucket-150x150-darkshadow.png'))

        # provision windows:
        for window in ["main", "view", "add"]:
            # create menus
            self.create_menu(self.windows[window], self.windows)
            # assign canned response app icon to each window:
            self.windows[window].iconphoto(False, logo_img)
            # create the bottom frames on view/add windows which hold the home button:
            if window != "main":
                BottomFrame(self.windows[window], self.windows)
        # configure the buttons on the main window:
        self.windows["main"].buttons["view"]["command"] = lambda: self.windows['view'].view_stored_responses()
        self.windows["main"].buttons["add"]["command"] = lambda: self.change_window(
            self.windows['main'], self.windows['add'])

        # for every window - if any window is closed - popup ask the user if they're sure
        for window in ["main", "view", "add"]:
            if window.lower() != "settings":
                self.windows[window].protocol(
                    "WM_DELETE_WINDOW", lambda s=self: self.on_closing(s.windows[window]))

    def on_closing(self, window):
        if tkinter.messagebox.askokcancel("Warning", "Are you sure you want to close the application?"):
            window.destroy()
        # destroy whole app
            try:
                self.windows["main"].destroy()
            except Exception as e:
                print("tried to delete main window")

    def _run_program(self):
        # run the mainloop of root/main window
        self.windows["main"].mainloop()


if __name__ == "__main__":
    ticket_bucket = TicketApplication()
    ticket_bucket._run_program()
