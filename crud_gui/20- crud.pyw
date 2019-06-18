# CRUD GUI
# Ignorar Id a la hora de insertar registros, RUD por Id (read, luego U o D).
# CRUD: Crear, leer, actualizar, borrar, igual que los botones.
# botones Create, Read, Update, Delete, con ventanas informativas.

import tkinter
from tkinter import messagebox
import sqlite3
import os

FRAME_BGCOLOR = "#ccccff"
BUTTON_A_BGCOLOR = "#768CCE"
BUTTON_BGCOLOR = "#BCC7E8"
DB_NAME = os.path.join("crud_gui", "crud.sqlite3")
ICON_NAME = os.path.join("icons", "crud.ico")


# DB menu
def connect_to_db():
    global conn
    global my_cursor

    conn = sqlite3.connect(DB_NAME)
    my_cursor = conn.cursor()
    # Create table if not exists
    # It would be better using CREATE TABLE IF NOT EXISTS USERS
    # but we are required to catch the exception
    try:
        my_cursor.execute("""
            CREATE TABLE USERS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR(50),
                PASSWORD VARCHAR(20),
                SURNAME VARCHAR(50),
                ADDRESS VARCHAR(50),
                COMMENT VARCHAR(100))
        """)
    except:
        messagebox.showwarning("DB",
                               "Database already exists.")
    else:
        messagebox.showinfo("DB",
                            "Database created successfully.")
    button_create.config(state=tkinter.NORMAL)
    button_read.config(state=tkinter.NORMAL)
    button_update.config(state=tkinter.NORMAL)
    button_delete.config(state=tkinter.NORMAL)
    menu_bar.entryconfigure(3, state=tkinter.NORMAL)


def confirm_exit():
    global conn
    global root

    answer = messagebox.askquestion("Exit",
                                    "Do you really want to exit?")
    if answer == "yes":
        try:
            conn.close()
        except:
            pass
        finally:
            root.destroy()


# Clean Menu
def clean_fields():
    user_id.set("")
    user_name.set("")
    # Another way to do it:
    # box_name.delete(0, tkinter.END)
    user_password.set("")
    user_surname.set("")
    user_address.set("")
    box_comment.delete(1.0, tkinter.END)


# CRUD Menu
def create_user():
    pass


def read_user():
    pass


def update_user():
    pass


def delete_user():
    pass


# Help Menu
def info_about():
    messagebox.showinfo("Acerca de", "CRUD GUI App\n\
Alucebur, 2019")


def info_license():
    messagebox.showwarning("License",
                           "This program is unlicensed.\n\
Feel free to use this code as you wish.")

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
main_frame.pack()
top_frame.pack()
bottom_frame.pack()

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

# Password
label_password = tkinter.Label(top_frame, text="Password:")
label_password.config(bg=FRAME_BGCOLOR, font=("Garamond", 12))
label_password.grid(row=2, column=0, sticky="e", pady=10, padx=10)

user_password = tkinter.StringVar()
box_password = tkinter.Entry(top_frame, textvariable=user_password)
box_password.grid(row=2, column=1, sticky="w", pady=10, padx=0)
box_password.config(fg="black", justify="center", show="*")

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
button_create.grid(row=6, column=0, sticky="w", pady=10, padx=10)

button_read = tkinter.Button(bottom_frame, text="Read",
                             activebackground=BUTTON_A_BGCOLOR,
                             bg=BUTTON_BGCOLOR,
                             state=tkinter.DISABLED,
                             command=read_user)
button_read.grid(row=6, column=1, sticky="w", pady=10, padx=10)

button_update = tkinter.Button(bottom_frame, text="Update",
                               activebackground=BUTTON_A_BGCOLOR,
                               bg=BUTTON_BGCOLOR,
                               state=tkinter.DISABLED,
                               command=update_user)
button_update.grid(row=6, column=2, sticky="w", pady=10, padx=10)

button_delete = tkinter.Button(bottom_frame, text="Delete",
                               activebackground=BUTTON_A_BGCOLOR,
                               bg=BUTTON_BGCOLOR,
                               state=tkinter.DISABLED,
                               command=delete_user)
button_delete.grid(row=6, column=3, sticky="w", pady=10, padx=10)

root.mainloop()
