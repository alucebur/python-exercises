"""
Stores info provided by the user in a local sqlite database,
and let them retrieve, change or delete such info.
Password is hashed for security reasons so it can't be retrieved.
"""
import tkinter
from tkinter import messagebox
import sqlite3
import os
import security as sec

FRAME_BGCOLOR = "#ccccff"
BUTTON_A_BGCOLOR = "#768CCE"
BUTTON_BGCOLOR = "#BCC7E8"
DB_NAME = os.path.join("crud_gui", "crud.sqlite3")
ICON_NAME = os.path.join("icons", "crud.ico")


class App():
    """
    Controller, builds graphic interface (self.root) and
    connection to database (self.conn)
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.root = tkinter.Tk()
        self.root.title("CRUD GUI")
        self.root.resizable(False, False)  # Width, Height
        self.root.iconbitmap(ICON_NAME)
        container = tkinter.Frame(self.root)
        container.parent = self.root
        container.config(pady=10, padx=10, bg=FRAME_BGCOLOR)
        container.pack()

        # Control variables
        self.user_id = tkinter.StringVar()
        self.user_name = tkinter.StringVar()
        self.user_password = tkinter.StringVar()
        self.user_surname = tkinter.StringVar()
        self.user_address = tkinter.StringVar()
        self.check_pass = tkinter.IntVar()

        # Frames
        self.root.frames = {}

        top_frame = DataField(container, self)
        self.root.frames[DataField] = top_frame

        bottom_frame = ButtonArea(container, self)
        self.root.frames[ButtonArea] = bottom_frame

        status_frame = StatusBar(container, self)
        self.root.frames[StatusBar] = status_frame

        # Menu bar
        self.root.menu_bar = MenuBar(self.root, self)
        self.root.config(menu=self.root.menu_bar)

        self.root.mainloop()

    # DB menu
    def connect_to_db(self):
        """
        Connects to the db, creating it and the table users if they
        don't exist. By doing so, enables CRUD menu and buttons.
        """
        try:
            # If DB doesn't exist, will be created
            #   (open in rwc mode by default)
            # We can avoid this by using a URI:
            #   DB_URI = f"file:{DB_NAME}?mode=rw"
            #   conn = sqlite3.connect(DB_URI, uri=True)
            self.conn = sqlite3.connect(self.db_name)
        except sqlite3.OperationalError:
            messagebox.showwarning("DB",
                                   "Connection could not be established.")
        else:
            self.cursor = self.conn.cursor()
            messagebox.showinfo("DB",
                                "Connection established successfully.")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name text,
                    password text,
                    surname text,
                    address text,
                    comment text)
            """)
            # Enable buttons and CRUD menu
            self.root.frames[ButtonArea].button_create.config(
                state=tkinter.NORMAL)
            self.root.frames[ButtonArea].button_read.config(
                state=tkinter.NORMAL)
            self.root.frames[ButtonArea].button_update.config(
                state=tkinter.NORMAL)
            self.root.frames[ButtonArea].button_delete.config(
                state=tkinter.NORMAL)
            self.root.menu_bar.entryconfigure(3, state=tkinter.NORMAL)

    def confirm_exit(self):
        """
        Closes the program after user agreement.
        """
        answer = messagebox.askquestion("Exit",
                                        "Do you really want to exit?")
        if answer == "yes":
            try:
                self.conn.close()
            except NameError:  # DB connection was not established
                pass
            finally:
                self.root.destroy()

    def clean_fields(self):
        """
        Cleans all fields of the form.
        """
        self.user_id.set("")
        self.user_name.set("")
        # Another way to do it:
        # self.root.frames[DataField].box_name.delete(0, tkinter.END)
        self.user_password.set("")
        self.user_surname.set("")
        self.user_address.set("")
        self.root.frames[DataField].box_comment.delete(1.0, tkinter.END)
        self.check_pass.set(0)

    # CRUD Menu
    def create_user(self):
        """
        Inserts data from the form into the database.
        """
        name = self.user_name.get()
        password = self.user_password.get()
        surname = self.user_surname.get()
        address = self.user_address.get()
        comment = self.root.frames[DataField].box_comment.get(
            1.0, tkinter.END)
        if ((name != "") and (password != "") and
                (surname != "") and (address != "")):
            sec_password = sec.encrypt_password(password)
            user_info = (name, sec_password, surname, address, comment)
            # We ignore ID since it is set autoincremental
            self.cursor.execute("INSERT INTO users VALUES (NULL,?,?,?,?,?)",
                                user_info)
            self.conn.commit()
            messagebox.showinfo("Create",
                                "User info has been added successfully")
        else:
            messagebox.showwarning("Create",
                                   "Please fill in all the fields.\n\
ID field will be ignored.")

    def show_user_info(self, tuple_id):
        """
        Retrieves data from the database and shows it.
        Returns error=True if data could not be retrieved.
        """
        error = False
        self.cursor.execute("""SELECT name,
                                      surname,
                                      address,
                                      comment
                               FROM users WHERE user_id=?""", tuple_id)
        user_info = self.cursor.fetchone()
        if user_info:  # empty sequences are false
            self.user_name.set(user_info[0])
            self.user_password.set('')  # It is hashed
            self.user_surname.set(user_info[1])
            self.user_address.set(user_info[2])
            self.root.frames[DataField].box_comment.delete(
                1.0, tkinter.END)
            self.root.frames[DataField].box_comment.insert(
                1.0, user_info[3])
        else:
            error = True
        return error

    def read_user(self):
        """
        Calls show_user_info to retrieve data from the requested
        user and/or display informative pop-ups of the process.
        """
        id_ = self.user_id.get()
        if id_ != "":
            error = self.show_user_info((id_,))
            if not error:
                messagebox.showinfo("Read",
                                    "User info has been retrieved \
successfully.")
            else:
                self.clean_fields()
                messagebox.showwarning("Read",
                                       "Sorry there is no user with \
the given ID.")
        else:
            messagebox.showwarning("Read", "Please fill in the ID field.")

    def update_user(self):
        """
        Modifies data from the user that matches the given user_id.
        """
        error = False
        id_ = self.user_id.get()
        name = self.user_name.get()
        password = self.user_password.get()
        surname = self.user_surname.get()
        address = self.user_address.get()
        comment = self.root.frames[DataField].box_comment.get(1.0, tkinter.END)
        if ((id_ != "") and (name != "") and
                (surname != "") and (address != "")):
            if self.check_pass.get() == 1 and (password != ""):
                sec_password = sec.encrypt_password(password)
                user_info = (name, sec_password, surname,
                             address, comment, id_)
                sql = """UPDATE users SET name= ?, password=?, surname=?,
                                          address=?, comment=?
                                      WHERE user_id=?"""
            elif self.check_pass.get() == 1:
                error = True
                messagebox.showwarning("Update", "Please fill password \
field.")
            else:  # Not password updated
                user_info = (name, surname, address, comment, id_)
                sql = """UPDATE users SET name= ?, surname=?,
                                          address=?, comment=?
                                      WHERE user_id=?"""
            if not error:
                self.cursor.execute(sql, user_info)
                self.conn.commit()
                changes = self.cursor.rowcount  # Number of rows updated
                if changes != 0:
                    messagebox.showinfo("Update",
                                        "User info has been updated \
successfully.")
                else:
                    self.clean_fields()
                    messagebox.showwarning("Update",
                                           "Sorry there is no user \
with the given ID.")
        else:
            messagebox.showwarning("Update",
                                   "Please fill in all the fields.")

    def delete_user(self):
        """
        Completely removes all data of the given user from the database.
        """
        error = False
        id_ = self.user_id.get()
        if id_ != "":
            # Shows user info
            error = self.show_user_info((id_,))
            if error:
                self.clean_fields()
                messagebox.showwarning("Delete",
                                       "Sorry there is no user with \
the given ID.")
            else:
                answer = messagebox.askquestion("Delete",
                                                "You are trying to \
delete this user.\nAre you sure?")
                if answer == "yes":
                    self.cursor.execute("DELETE FROM users WHERE user_id=?",
                                        (id_,))
                    self.conn.commit()
                    self.clean_fields()
                    messagebox.showinfo("Delete",
                                        "User has been deleted successfully.")
        else:
            messagebox.showwarning("Delete", "Please fill in the ID field.")

    # Help Menu
    @staticmethod
    def info_about():
        """
        Displays About info.
        """
        messagebox.showinfo("Acerca de", "CRUD GUI App\nAlucebur, 2019")

    @staticmethod
    def info_license():
        """
        Displays License info.
        """
        messagebox.showwarning("License",
                               "This program is unlicensed.\n\
Feel free to use this code at your pleasure.")


class DataField(tkinter.Frame):
    """
    Frame with text fields
    """
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.config(bg=FRAME_BGCOLOR)
        self.pack()

        # Id
        self.label_id = tkinter.Label(self, text="Id:")
        self.label_id.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
        self.label_id.grid(row=0, column=0, sticky="e", pady=10, padx=10)

        self.box_id = tkinter.Entry(self, textvariable=controller.user_id)
        self.box_id.grid(row=0, column=1, sticky="w", pady=10, padx=0)
        self.box_id.config(fg="red", justify="center")

        # Name
        self.label_name = tkinter.Label(self, text="Name:")
        self.label_name.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
        self.label_name.grid(row=1, column=0, sticky="e", pady=10, padx=10)

        self.box_name = tkinter.Entry(self, textvariable=controller.user_name)
        self.box_name.grid(row=1, column=1, sticky="w", pady=10, padx=0)
        self.box_name.config(fg="black", justify="center")

        # Password
        self.label_password = tkinter.Label(self, text="Password:")
        self.label_password.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
        self.label_password.grid(row=2, column=0, sticky="e", pady=10, padx=10)

        self.box_password = tkinter.Entry(
            self, textvariable=controller.user_password)
        self.box_password.grid(row=2, column=1, sticky="w", pady=10, padx=0)
        self.box_password.config(fg="black", justify="center", show="*")

        self.checkbutton_pass = tkinter.Checkbutton(
            self, text="U", variable=controller.check_pass,
            onvalue=1, offvalue=0)
        self.checkbutton_pass.config(bg=FRAME_BGCOLOR,
                                     activebackground=FRAME_BGCOLOR,
                                     font=("Garamond", 12))
        self.checkbutton_pass.grid(row=2, column=3,
                                   sticky="w", pady=10, padx=10)
        self.checkbutton_pass.bind("<Enter>", self.__display_help)
        self.checkbutton_pass.bind("<Leave>", self.__remove_help)

        # Surname
        self.label_surname = tkinter.Label(self, text="Surname:")
        self.label_surname.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
        self.label_surname.grid(row=3, column=0, sticky="e", pady=10, padx=10)

        self.box_surname = tkinter.Entry(
            self, textvariable=controller.user_surname)
        self.box_surname.grid(row=3, column=1, sticky="w", pady=10, padx=0)
        self.box_surname.config(fg="black", justify="center")

        # Address
        self.label_address = tkinter.Label(self, text="Address:")
        self.label_address.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
        self.label_address.grid(row=4, column=0, sticky="e", pady=10, padx=10)

        self.box_address = tkinter.Entry(
            self, textvariable=controller.user_address)
        self.box_address.grid(row=4, column=1, sticky="w", pady=10, padx=0)
        self.box_address.config(fg="black", justify="center")

        # Comment
        self.label_comment = tkinter.Label(self, text="Comment:")
        self.label_comment.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
        self.label_comment.grid(row=5, column=0, sticky="e",
                                pady=10, padx=10)

        self.box_comment = tkinter.Text(self, width=15, height=5,
                                        wrap=tkinter.WORD)
        self.box_comment.grid(row=5, column=1, sticky="w",
                              pady=10, padx=0)
        self.box_comment.config(fg="black")

        self.scroll_vert = tkinter.Scrollbar(self,
                                             command=self.box_comment.yview)
        self.scroll_vert.grid(row=5, column=2, sticky="nsew",
                              pady=10, padx=0)
        self.box_comment.config(yscrollcommand=self.scroll_vert.set)

    def __display_help(self, event):
        self.controller.root.frames[StatusBar].label_status.configure(
            text="Update password")

    def __remove_help(self, event):
        self.controller.root.frames[StatusBar].label_status.configure(
            text="")


class ButtonArea(tkinter.LabelFrame):
    """
    Frame with buttons
    """
    def __init__(self, parent, controller):
        tkinter.LabelFrame.__init__(self, parent, text="CRUD")
        self.parent = parent
        self.config(bg=FRAME_BGCOLOR)
        self.pack()

        # Buttons
        self.button_create = tkinter.Button(
            self,
            text="Create",
            activebackground=BUTTON_A_BGCOLOR,
            bg=BUTTON_BGCOLOR,
            state=tkinter.DISABLED,
            command=controller.create_user)
        self.button_create.grid(row=0, column=0, sticky="w", pady=10, padx=10)

        self.button_read = tkinter.Button(
            self,
            text="Read",
            activebackground=BUTTON_A_BGCOLOR,
            bg=BUTTON_BGCOLOR,
            state=tkinter.DISABLED,
            command=controller.read_user)
        self.button_read.grid(row=0, column=1, sticky="w", pady=10, padx=10)

        self.button_update = tkinter.Button(
            self,
            text="Update",
            activebackground=BUTTON_A_BGCOLOR,
            bg=BUTTON_BGCOLOR,
            state=tkinter.DISABLED,
            command=controller.update_user)
        self.button_update.grid(row=0, column=2, sticky="w", pady=10, padx=10)

        self.button_delete = tkinter.Button(
            self,
            text="Delete",
            activebackground=BUTTON_A_BGCOLOR,
            bg=BUTTON_BGCOLOR,
            state=tkinter.DISABLED,
            command=controller.delete_user)
        self.button_delete.grid(row=0, column=3, sticky="w", pady=10, padx=10)


class StatusBar(tkinter.Frame):
    """
    Frame that displays messages at the bottom of the app
    """
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.config(bg=FRAME_BGCOLOR)
        self.pack()
        self.label_status = tkinter.Label(self, text="")
        self.label_status.config(bg=FRAME_BGCOLOR, font=("Garamond", 10))
        self.label_status.grid(row=0, column=0, sticky="e",
                               pady=10, padx=10)


class MenuBar(tkinter.Menu):
    """
    Menu bar
    """
    def __init__(self, parent, controller):
        tkinter.Menu.__init__(self, parent)
        self.parent = parent

        self.menu_db = tkinter.Menu(self, tearoff=0)
        self.menu_db.add_command(label="Connect",
                                 command=controller.connect_to_db)
        self.menu_db.add_separator()
        self.menu_db.add_command(label="Exit",
                                 command=controller.confirm_exit)

        self.menu_clean = tkinter.Menu(tearoff=0)
        self.menu_clean.add_command(label="Clean fields",
                                    command=controller.clean_fields)

        self.menu_crud = tkinter.Menu(tearoff=0)
        self.menu_crud.add_command(label="Create",
                                   command=controller.create_user)
        self.menu_crud.add_command(label="Read",
                                   command=controller.read_user)
        self.menu_crud.add_command(label="Update",
                                   command=controller.update_user)
        self.menu_crud.add_command(label="Delete",
                                   command=controller.delete_user)

        self.menu_help = tkinter.Menu(tearoff=0)
        self.menu_help.add_command(label="License",
                                   command=controller.info_license)
        self.menu_help.add_command(label="About",
                                   command=controller.info_about)

        self.add_cascade(label="DB", menu=self.menu_db)
        self.add_cascade(label="Clean", menu=self.menu_clean)
        self.add_cascade(label="CRUD", menu=self.menu_crud,
                         state=tkinter.DISABLED)
        self.add_cascade(label="Help", menu=self.menu_help)


def main():
    App(DB_NAME)

if __name__ == '__main__':
    main()
