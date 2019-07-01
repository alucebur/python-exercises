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


# DB menu
def connect_to_db():
    """
    Connects to the db, creating it and the table users if they don't exist.
    By doing so, enables CRUD menu and buttons.
    """
    global conn
    global my_cursor

    try:
        # If DB doesn't exist, it will create it (open in rwc mode by default)
        # We can avoid this by using a URI:
        #   DB_URI = f"file:{DB_NAME}?mode=rw"
        #   conn = sqlite3.connect(DB_URI, uri=True)
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.OperationalError:
        messagebox.showwarning("DB",
                               "Connection could not be established.")
    else:
        my_cursor = conn.cursor()
        messagebox.showinfo("DB",
                            "Connection established successfully.")
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text,
                password text,
                surname text,
                address text,
                comment text)
        """)
        # Enable buttons and CRUD menu
        button_create.config(state=tkinter.NORMAL)
        button_read.config(state=tkinter.NORMAL)
        button_update.config(state=tkinter.NORMAL)
        button_delete.config(state=tkinter.NORMAL)
        menu_bar.entryconfigure(3, state=tkinter.NORMAL)


def confirm_exit():
    """
    Closes the program after user agreement.
    """
    answer = messagebox.askquestion("Exit",
                                    "Do you really want to exit?")
    if answer == "yes":
        try:
            conn.close()
        except NameError:  # DB connection was not established
            pass
        finally:
            root.destroy()


def clean_fields():
    """
    Cleans all fields of the form.
    """
    user_id.set("")
    user_name.set("")
    # Another way to do it:
    # box_name.delete(0, tkinter.END)
    user_password.set("")
    user_surname.set("")
    user_address.set("")
    box_comment.delete(1.0, tkinter.END)
    check_pass.set(0)


# CRUD Menu
def create_user():
    """
    Inserts data from the form into the database.
    """
    name = user_name.get()
    password = user_password.get()
    surname = user_surname.get()
    address = user_address.get()
    comment = box_comment.get(1.0, tkinter.END)
    if ((name != "") and (password != "") and
            (surname != "") and (address != "")):
        sec_password = sec.encrypt_password(password)
        user_info = (name, sec_password, surname, address, comment)
        # We ignore ID since it is set autoincremental
        my_cursor.execute("INSERT INTO users VALUES (NULL,?,?,?,?,?)",
                          user_info)
        conn.commit()
        messagebox.showinfo("Create",
                            "User info has been added successfully")
    else:
        messagebox.showwarning("Create",
                               "Please fill in all the fields.\n\
ID field will be ignored.")


def show_user_info(tuple_id):
    """
    Retrieves data from the database and shows it.
    Returns error=True if data could not be retrieved.
    """
    error = False
    my_cursor.execute("""SELECT name,
                                surname,
                                address,
                                comment
                         FROM users WHERE user_id=?""", tuple_id)
    user_info = my_cursor.fetchone()
    if user_info:  # empty sequences are false
        user_name.set(user_info[0])
        user_password.set('')  # It is hashed
        user_surname.set(user_info[1])
        user_address.set(user_info[2])
        box_comment.delete(1.0, tkinter.END)
        box_comment.insert(1.0, user_info[3])
    else:
        error = True
    return error


def read_user():
    """
    Calls show_user_info to retrieve data from the requested user and/or
    display informative pop-ups of the process.
    """
    id_ = user_id.get()
    if id_ != "":
        error = show_user_info((id_,))
        if not error:
            messagebox.showinfo("Read",
                                "User info has been retrieved successfully.")
        else:
            clean_fields()
            messagebox.showwarning("Read",
                                   "Sorry there is no user with the given ID.")
    else:
        messagebox.showwarning("Read", "Please fill in the ID field.")


def update_user():
    """
    Modifies data from the user that matches the given user_id.
    """
    error = False
    id_ = user_id.get()
    name = user_name.get()
    password = user_password.get()
    surname = user_surname.get()
    address = user_address.get()
    comment = box_comment.get(1.0, tkinter.END)
    if ((id_ != "") and (name != "") and
            (surname != "") and (address != "")):
        if check_pass.get() == 1 and (password != ""):
            sec_password = sec.encrypt_password(password)
            user_info = (name, sec_password, surname, address, comment, id_)
            sql = """UPDATE users SET name= ?, password=?, surname=?,
                                      address=?, comment=?
                                  WHERE user_id=?"""
        elif check_pass.get() == 1:
            error = True
            messagebox.showwarning("Update", "Please fill password field.")
        else:  # Not password updated
            user_info = (name, surname, address, comment, id_)
            sql = """UPDATE users SET name= ?, surname=?,
                                      address=?, comment=?
                                  WHERE user_id=?"""
        if not error:
            my_cursor.execute(sql, user_info)
            conn.commit()
            changes = my_cursor.rowcount  # Number of rows updated
            if changes != 0:
                messagebox.showinfo("Update",
                                    "User info has been updated successfully.")
            else:
                clean_fields()
                messagebox.showwarning("Update",
                                       "Sorry there is no user with the \
given ID.")
    else:
        messagebox.showwarning("Update", "Please fill in all the fields.")


def delete_user():
    """
    Completely removes all data of the given user from the database.
    """
    error = False
    id_ = user_id.get()
    if id_ != "":
        # Shows user info
        error = show_user_info((id_,))
        if error:
            clean_fields()
            messagebox.showwarning("Delete",
                                   "Sorry there is no user with the given ID.")
        else:
            answer = messagebox.askquestion("Delete",
                                            "You are trying to delete \
this user.\nAre you sure?")
            if answer == "yes":
                my_cursor.execute("DELETE FROM users WHERE user_id=?", (id_,))
                conn.commit()
                clean_fields()
                messagebox.showinfo("Delete",
                                    "User has been deleted successfully.")
    else:
        messagebox.showwarning("Delete", "Please fill in the ID field.")


# Help Menu
def info_about():
    """
    Displays About info.
    """
    messagebox.showinfo("Acerca de", "CRUD GUI App\nAlucebur, 2019")


def info_license():
    """
    Displays License info.
    """
    messagebox.showwarning("License",
                           "This program is unlicensed.\n\
Feel free to use this code at your pleasure.")

root = tkinter.Tk()
root.title("CRUD GUI")
root.resizable(False, False)  # Width, Height
root.iconbitmap(ICON_NAME)
main_frame = tkinter.Frame(root)
main_frame.config(pady=10, padx=10, bg=FRAME_BGCOLOR)
top_frame = tkinter.Frame(main_frame)
top_frame.config(bg=FRAME_BGCOLOR)
bottom_frame = tkinter.LabelFrame(main_frame, text="CRUD")
bottom_frame.config(bg=FRAME_BGCOLOR)
status_frame = tkinter.Frame(main_frame)
status_frame.config(bg=FRAME_BGCOLOR)
main_frame.pack()
top_frame.pack()
bottom_frame.pack()
status_frame.pack()

# Menu bar
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)

menu_db = tkinter.Menu(menu_bar, tearoff=0)
menu_db.add_command(label="Connect", command=connect_to_db)
menu_db.add_separator()
menu_db.add_command(label="Exit", command=confirm_exit)

menu_clean = tkinter.Menu(menu_bar, tearoff=0)
menu_clean.add_command(label="Clean fields", command=clean_fields)

menu_crud = tkinter.Menu(menu_bar, tearoff=0)
menu_crud.add_command(label="Create", command=create_user)
menu_crud.add_command(label="Read", command=read_user)
menu_crud.add_command(label="Update", command=update_user)
menu_crud.add_command(label="Delete", command=delete_user)

menu_help = tkinter.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="License", command=info_license)
menu_help.add_command(label="About", command=info_about)

menu_bar.add_cascade(label="DB", menu=menu_db)
menu_bar.add_cascade(label="Clean", menu=menu_clean)
menu_bar.add_cascade(label="CRUD", menu=menu_crud, state=tkinter.DISABLED)
menu_bar.add_cascade(label="Help", menu=menu_help)

# Id
label_id = tkinter.Label(top_frame, text="Id:")
label_id.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
label_id.grid(row=0, column=0, sticky="e", pady=10, padx=10)

user_id = tkinter.StringVar()
box_id = tkinter.Entry(top_frame, textvariable=user_id)
box_id.grid(row=0, column=1, sticky="w", pady=10, padx=0)
box_id.config(fg="red", justify="center")

# Name
label_name = tkinter.Label(top_frame, text="Name:")
label_name.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
label_name.grid(row=1, column=0, sticky="e", pady=10, padx=10)

user_name = tkinter.StringVar()
box_name = tkinter.Entry(top_frame, textvariable=user_name)
box_name.grid(row=1, column=1, sticky="w", pady=10, padx=0)
box_name.config(fg="black", justify="center")


def display_help(event):
    label_status.configure(text="Update password")


def remove_help(event):
    label_status.configure(text="")

# Password
label_password = tkinter.Label(top_frame, text="Password:")
label_password.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
label_password.grid(row=2, column=0, sticky="e", pady=10, padx=10)

user_password = tkinter.StringVar()
box_password = tkinter.Entry(top_frame, textvariable=user_password)
box_password.grid(row=2, column=1, sticky="w", pady=10, padx=0)
box_password.config(fg="black", justify="center", show="*")

check_pass = tkinter.IntVar()
checkbutton_pass = tkinter.Checkbutton(top_frame, text="U",
                                       variable=check_pass,
                                       onvalue=1, offvalue=0)
checkbutton_pass.config(bg=FRAME_BGCOLOR, activebackground=FRAME_BGCOLOR,
                        font=("Garamond", 12))
checkbutton_pass.grid(row=2, column=3, sticky="w", pady=10, padx=10)
label_status = tkinter.Label(status_frame, text="")
label_status.config(bg=FRAME_BGCOLOR, font=("Garamond", 10))
label_status.grid(row=0, column=0, sticky="e", pady=10, padx=10)
checkbutton_pass.bind("<Enter>", display_help)
checkbutton_pass.bind("<Leave>", remove_help)

# Surname
label_surname = tkinter.Label(top_frame, text="Surname:")
label_surname.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
label_surname.grid(row=3, column=0, sticky="e", pady=10, padx=10)

user_surname = tkinter.StringVar()
box_surname = tkinter.Entry(top_frame, textvariable=user_surname)
box_surname.grid(row=3, column=1, sticky="w", pady=10, padx=0)
box_surname.config(fg="black", justify="center")

# Address
label_address = tkinter.Label(top_frame, text="Address:")
label_address.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
label_address.grid(row=4, column=0, sticky="e", pady=10, padx=10)

user_address = tkinter.StringVar()
box_address = tkinter.Entry(top_frame, textvariable=user_address)
box_address.grid(row=4, column=1, sticky="w", pady=10, padx=0)
box_address.config(fg="black", justify="center")

# Comment
label_comment = tkinter.Label(top_frame, text="Comment:")
label_comment.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
label_comment.grid(row=5, column=0, sticky="e", pady=10, padx=10)

box_comment = tkinter.Text(top_frame, width=15, height=5, wrap=tkinter.WORD)
box_comment.grid(row=5, column=1, sticky="w", pady=10, padx=0)
box_comment.config(fg="black")

scroll_vert = tkinter.Scrollbar(top_frame, command=box_comment.yview)
scroll_vert.grid(row=5, column=2, sticky="nsew", pady=10, padx=0)
box_comment.config(yscrollcommand=scroll_vert.set)

# Buttons
button_create = tkinter.Button(bottom_frame, text="Create",
                               activebackground=BUTTON_A_BGCOLOR,
                               bg=BUTTON_BGCOLOR,
                               state=tkinter.DISABLED,
                               command=create_user)
button_create.grid(row=0, column=0, sticky="w", pady=10, padx=10)

button_read = tkinter.Button(bottom_frame, text="Read",
                             activebackground=BUTTON_A_BGCOLOR,
                             bg=BUTTON_BGCOLOR,
                             state=tkinter.DISABLED,
                             command=read_user)
button_read.grid(row=0, column=1, sticky="w", pady=10, padx=10)

button_update = tkinter.Button(bottom_frame, text="Update",
                               activebackground=BUTTON_A_BGCOLOR,
                               bg=BUTTON_BGCOLOR,
                               state=tkinter.DISABLED,
                               command=update_user)
button_update.grid(row=0, column=2, sticky="w", pady=10, padx=10)

button_delete = tkinter.Button(bottom_frame, text="Delete",
                               activebackground=BUTTON_A_BGCOLOR,
                               bg=BUTTON_BGCOLOR,
                               state=tkinter.DISABLED,
                               command=delete_user)
button_delete.grid(row=0, column=3, sticky="w", pady=10, padx=10)

root.mainloop()
