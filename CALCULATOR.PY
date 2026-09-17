import tkinter as tk
from tkinter import messagebox
import math

history = []
current = ""
expression = ""
last_result = None


def format_number(value):
    if isinstance(value, str):
        return value
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error"
    return a / b


def power(a, b):
    return a ** b


def remainder(a, b):
    if b == 0:
        return "Error"
    return a % b


def square_root(a):
    if a < 0:
        return "Error"
    return math.sqrt(a)


def square(a):
    return a ** 2


def cube(a):
    return a ** 3


def factorial(a):
    if a < 0 or not a.is_integer():
        return "Error"
    return math.factorial(int(a))


def save_history(calculation, result):
    history.append(f"{calculation} = {format_number(result)}")


def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculator History")
    history_window.geometry("430x450")
    history_window.configure(bg="#111111")
    history_window.resizable(False, False)

    tk.Label(
        history_window,
        text="CALCULATOR HISTORY",
        font=("Segoe UI", 18, "bold"),
        fg="#00ff9d",
        bg="#111111"
    ).pack(pady=(18, 10))

    frame = tk.Frame(history_window, bg="#111111")
    frame.pack(fill="both", expand=True, padx=18, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(
        frame,
        yscrollcommand=scrollbar.set,
        font=("Consolas", 12),
        bg="#1b1b1b",
        fg="white",
        selectbackground="#00a86b",
        borderwidth=0,
        highlightthickness=0
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    if history:
        for number, calculation in enumerate(history, start=1):
            listbox.insert("end", f"{number}. {calculation}")
    else:
        listbox.insert("end", "No calculations yet.")

    tk.Button(
        history_window,
        text="Close",
        command=history_window.destroy,
        font=("Segoe UI", 11, "bold"),
        bg="#252525",
        fg="white",
        activebackground="#333333",
        activeforeground="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=15)


def clear_history():
    history.clear()
    messagebox.showinfo("History", "History cleared!")


def update_display():
    display_var.set(expression if expression else "0")


def clear():
    global expression
    expression = ""
    update_display()


def backspace():
    global expression
    expression = expression[:-1]
    update_display()


def append_number(number):
    global expression

    if expression == "0":
        expression = number
    else:
        expression += number

    update_display()


def append_decimal():
    global expression

    current_number = expression.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").replace("%", " ").split()[-1] if expression else ""

    if "." not in current_number:
        if not expression or expression[-1] in "+-*/%":
            expression += "0."
        else:
            expression += "."

    update_display()


def append_operator(operator):
    global expression

    if not expression:
        return

    if expression[-1] in "+-*/%":
        expression = expression[:-1] + operator
    else:
        expression += operator

    update_display()


def calculate():
    global expression, last_result

    if not expression:
        return

    try:
        result = eval(expression, {"__builtins__": {}}, {})

        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError

        save_history(expression, result)
        last_result = result
        expression = format_number(result)
        update_display()

    except ZeroDivisionError:
        show_error("Cannot divide by zero!")
    except Exception:
        show_error("Invalid calculation.")


def show_error(message):
    global expression
    messagebox.showerror("Calculator Error", message)
    expression = ""
    update_display()


def unary_operation(operation, symbol):
    global expression, last_result

    if not expression:
        return

    try:
        value = float(eval(expression, {"__builtins__": {}}, {}))
        result = operation(value)

        if isinstance(result, str):
            show_error(result)
            return

        save_history(f"{symbol}{format_number(value)}", result)
        last_result = result
        expression = format_number(result)
        update_display()

    except Exception as error:
        show_error(str(error))


def do_square_root():
    unary_operation(square_root, "√")


def do_square():
    unary_operation(square, "")


def do_cube():
    unary_operation(cube, "")


def do_factorial():
    unary_operation(factorial, "")


def do_power():
    append_operator("**")


def keyboard_input(event):
    key = event.keysym
    char = event.char

    if char.isdigit():
        append_number(char)
    elif char in "+-*/%":
        append_operator(char)
    elif char == ".":
        append_decimal()
    elif key in ("Return", "KP_Enter"):
        calculate()
    elif key == "BackSpace":
        backspace()
    elif key == "Escape":
        clear()



root = tk.Tk()
root.title("Calculator by Alexoukos/R3Z")
root.geometry("460x690")
root.minsize(400, 620)
root.configure(bg="#0b0b0b")

display_var = tk.StringVar(value="0")

header = tk.Frame(root, bg="#0b0b0b")
header.pack(fill="x", padx=22, pady=(20, 10))

tk.Label(
    header,
    text="CALCULATOR",
    font=("Segoe UI", 22, "bold"),
    fg="#00ff9d",
    bg="#0b0b0b"
).pack(side="left")

tk.Label(
    header,
    text="By Alexoukos/R3Z",
    font=("Segoe UI", 10, "bold"),
    fg="#777777",
    bg="#0b0b0b"
).pack(side="right", pady=7)

display_frame = tk.Frame(
    root,
    bg="#151515",
    highlightbackground="#292929",
    highlightthickness=1
)
display_frame.pack(fill="x", padx=20, pady=(5, 15))

display = tk.Entry(
    display_frame,
    textvariable=display_var,
    font=("Consolas", 30, "bold"),
    justify="right",
    bg="#151515",
    fg="white",
    insertbackground="white",
    relief="flat",
    bd=0
)
display.pack(fill="x", ipady=20, padx=15)
display.bind("<Key>", lambda e: "break")  

BUTTON_BG = "#202020"
BUTTON_ACTIVE = "#303030"
OPERATOR_BG = "#064d35"
OPERATOR_ACTIVE = "#08704b"
SPECIAL_BG = "#292929"
SPECIAL_ACTIVE = "#393939"
EQUAL_BG = "#00a86b"
EQUAL_ACTIVE = "#00c77e"

button_frame = tk.Frame(root, bg="#0b0b0b")
button_frame.pack(fill="both", expand=True, padx=20)

for i in range(6):
    button_frame.grid_columnconfigure(i, weight=1)

for i in range(7):
    button_frame.grid_rowconfigure(i, weight=1)


def make_button(text, row, col, command, bg=BUTTON_BG, active=BUTTON_ACTIVE, colspan=1):
    button = tk.Button(
        button_frame,
        text=text,
        command=command,
        font=("Segoe UI", 13, "bold"),
        bg=bg,
        fg="white",
        activebackground=active,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2"
    )
    button.grid(
        row=row,
        column=col,
        columnspan=colspan,
        sticky="nsew",
        padx=4,
        pady=4
    )
    return button


make_button("C", 0, 0, clear, SPECIAL_BG, SPECIAL_ACTIVE)
make_button("⌫", 0, 1, backspace, SPECIAL_BG, SPECIAL_ACTIVE)
make_button("History", 0, 2, show_history, SPECIAL_BG, SPECIAL_ACTIVE, 2)
make_button("Clear H.", 0, 4, clear_history, SPECIAL_BG, SPECIAL_ACTIVE, 2)

make_button("7", 1, 0, lambda: append_number("7"))
make_button("8", 1, 1, lambda: append_number("8"))
make_button("9", 1, 2, lambda: append_number("9"))
make_button("÷", 1, 3, lambda: append_operator("/"), OPERATOR_BG, OPERATOR_ACTIVE)
make_button("√", 1, 4, do_square_root, SPECIAL_BG, SPECIAL_ACTIVE)
make_button("x²", 1, 5, do_square, SPECIAL_BG, SPECIAL_ACTIVE)

make_button("4", 2, 0, lambda: append_number("4"))
make_button("5", 2, 1, lambda: append_number("5"))
make_button("6", 2, 2, lambda: append_number("6"))
make_button("×", 2, 3, lambda: append_operator("*"), OPERATOR_BG, OPERATOR_ACTIVE)
make_button("x³", 2, 4, do_cube, SPECIAL_BG, SPECIAL_ACTIVE)
make_button("xʸ", 2, 5, do_power, SPECIAL_BG, SPECIAL_ACTIVE)

make_button("1", 3, 0, lambda: append_number("1"))
make_button("2", 3, 1, lambda: append_number("2"))
make_button("3", 3, 2, lambda: append_number("3"))
make_button("−", 3, 3, lambda: append_operator("-"), OPERATOR_BG, OPERATOR_ACTIVE)
make_button("%", 3, 4, lambda: append_operator("%"), SPECIAL_BG, SPECIAL_ACTIVE)
make_button("!", 3, 5, do_factorial, SPECIAL_BG, SPECIAL_ACTIVE)

make_button("0", 4, 0, lambda: append_number("0"), colspan=2)
make_button(".", 4, 2, append_decimal)
make_button("+", 4, 3, lambda: append_operator("+"), OPERATOR_BG, OPERATOR_ACTIVE)
make_button("=", 4, 4, calculate, EQUAL_BG, EQUAL_ACTIVE, 2)

info = tk.Label(
    root,
    text="Enter / Backspace / Esc also work",
    font=("Segoe UI", 9),
    fg="#666666",
    bg="#0b0b0b"
)
info.pack(pady=(8, 12))

root.bind("<Key>", keyboard_input)
root.mainloop()
# GAMO THN DESPOINA 
