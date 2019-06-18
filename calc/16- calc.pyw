# Calculator
import tkinter as tk
import os

ICON_NAME = os.path.join("icons", "calc.ico")

root = tk.Tk()
root.title("Calculator")
root.resizable(False, False)  # Width, Height
root.iconbitmap(ICON_NAME)  # App icon
root.config(bg="grey")
frame = tk.Frame(root)
frame.pack()
frame.config(bg="lightgrey", relief="flat")

# ---- screen ----
t_screen = tk.StringVar()
operand1 = ""
operation = ""
reset_screen = False  # If true, it will reset screen next time
screen = tk.Entry(frame, textvariable=t_screen)
screen.grid(row=0, column=1, padx=10, pady=10, columnspan=4, ipady=5)
screen.config(bg="black", fg="#03f943", justify="right",
              font=("Cambria", 14))


# ---- functions ----
def number_pressed(num):
    global reset_screen
    has_coma = False
    if reset_screen:
        old_screen = "0"
        reset_screen = False
    else:
        old_screen = t_screen.get()
    for character in old_screen:
        if character == ',':
            has_coma = True
            break
    # Zeros on the left are not drawn
    if old_screen == "0" and num != ",":
        if num != "0":
            t_screen.set(num)
        else:
            t_screen.set("0")
    # Only one comma allowed
    elif num != "," or not has_coma:
        t_screen.set(old_screen + num)


def show_result(op1, op2, op):
    global operation
    global operand1
    # Local format of decimal numbers (3.14 -> 3,14)
    op1 = op1.replace(",", ".", 1)
    op2 = op2.replace(",", ".", 1)
    if op == "+":
        answer = str(float(op1) + float(op2))
    elif op == "-":
        answer = str(float(op1) - float(op2))
    elif op == "/":
        try:
            answer = str(float(op1) / float(op2))
        except ZeroDivisionError:
            answer = "ERROR DIV BY 0"
    elif op == "x":
        answer = str(float(op1) * float(op2))
    answer = answer.replace(".", ",", 1)
    # Remove decimal part if 0
    if answer[-2] == "," and answer[-1] == "0":
        answer = answer[0:-2]
    t_screen.set(answer)
    if answer != "ERROR DIV BY 0":
        operand1 = t_screen.get()
    else:
        operand1 = ""


def op_pressed(op):
    global operation
    global reset_screen
    global operand1
    old_screen = t_screen.get()
    if old_screen == "ERROR DIV BY 0":
        old_screen = "0"
        t_screen.set("0")
    if op == "C":
        reset_screen = False
        t_screen.set("0")
        operation = ""
        operand1 = ""
    elif op == "CE":
        reset_screen = False
        t_screen.set("0")
    elif op == "<":
        if reset_screen:
            old_screen = "0"
            reset_screen = False
        if len(old_screen) == 1:
            t_screen.set("0")
        else:
            t_screen.set(old_screen[0:-1])
    elif op == "+":
        if not reset_screen:
            reset_screen = True
            if operand1 != "" and operation != "":
                show_result(operand1, old_screen, operation)
            else:
                operand1 = old_screen
        operation = "+"
    elif op == "-":
        if not reset_screen:
            reset_screen = True
            if operand1 != "" and operation != "":
                show_result(operand1, old_screen, operation)
            else:
                operand1 = old_screen
        operation = "-"
    elif op == "/":
        if not reset_screen:
            reset_screen = True
            if operand1 != "" and operation != "":
                show_result(operand1, old_screen, operation)
            else:
                operand1 = old_screen
        operation = "/"
    elif op == "x":
        if not reset_screen:
            reset_screen = True
            if operand1 != "" and operation != "":
                show_result(operand1, old_screen, operation)
            else:
                operand1 = old_screen
        operation = "x"
    elif op == "=":
        if not reset_screen:
            reset_screen = True
            if operand1 != "" and operation != "":
                show_result(operand1, old_screen, operation)
            else:
                operand1 = ""
        operation = ""

# Screen starts as 0
number_pressed("0")

# ---- row 0 ----
# function lambda to avoid execution of op_pressed since it has ()
button_clean = tk.Button(frame, text="CE", width=6, height=2,
                         command=lambda: op_pressed("CE"))
button_clean.grid(row=1, column=2)
button_reset = tk.Button(frame, text="C", width=6, height=2,
                         command=lambda: op_pressed("C"))
button_reset.grid(row=1, column=3)
button_back = tk.Button(frame, text="<", width=6, height=2,
                        command=lambda: op_pressed("<"))
button_back.grid(row=1, column=4, padx=(0, 10))

# ---- row 1 ----
# function lambda to avoid execution of number_pressed since it has ()
button7 = tk.Button(frame, text="7", width=6, height=2,
                    command=lambda: number_pressed("7"))
button7.grid(row=2, column=1, padx=(10, 0))
button8 = tk.Button(frame, text="8", width=6, height=2,
                    command=lambda: number_pressed("8"))
button8.grid(row=2, column=2)
button9 = tk.Button(frame, text="9", width=6, height=2,
                    command=lambda: number_pressed("9"))
button9.grid(row=2, column=3)
button_div = tk.Button(frame, text="/", width=6, height=2,
                       command=lambda: op_pressed("/"))
button_div.grid(row=2, column=4, padx=(0, 10))

# ---- row 2----
button4 = tk.Button(frame, text="4", width=6, height=2,
                    command=lambda: number_pressed("4"))
button4.grid(row=3, column=1, padx=(10, 0))
button5 = tk.Button(frame, text="5", width=6, height=2,
                    command=lambda: number_pressed("5"))
button5.grid(row=3, column=2)
button6 = tk.Button(frame, text="6", width=6, height=2,
                    command=lambda: number_pressed("6"))
button6.grid(row=3, column=3)
button_mult = tk.Button(frame, text="x", width=6, height=2,
                        command=lambda: op_pressed("x"))
button_mult.grid(row=3, column=4, padx=(0, 10))

# ---- row 3 ----
button1 = tk.Button(frame, text="1", width=6, height=2,
                    command=lambda: number_pressed("1"))
button1.grid(row=4, column=1, padx=(10, 0))
button2 = tk.Button(frame, text="2", width=6, height=2,
                    command=lambda: number_pressed("2"))
button2.grid(row=4, column=2)
button3 = tk.Button(frame, text="3", width=6, height=2,
                    command=lambda: number_pressed("3"))
button3.grid(row=4, column=3)
button_subs = tk.Button(frame, text="-", width=6, height=2,
                        command=lambda: op_pressed("-"))
button_subs.grid(row=4, column=4, padx=(0, 10))

# ---- row 4 ----
button_comma = tk.Button(frame, text=",", width=6, height=2,
                         command=lambda: number_pressed(","))
button_comma.grid(row=5, column=1, padx=(10, 0), pady=(0, 10))
button0 = tk.Button(frame, text="0", width=6, height=2,
                    command=lambda: number_pressed("0"))
button0.grid(row=5, column=2, pady=(0, 10))
button_equal = tk.Button(frame, text="=", width=6, height=2,
                         command=lambda: op_pressed("="))
button_equal.grid(row=5, column=3, pady=(0, 10))
button_sum = tk.Button(frame, text="+", width=6, height=2,
                       command=lambda: op_pressed("+"))
button_sum.grid(row=5, column=4, pady=(0, 10), padx=(0, 10))

root.mainloop()
