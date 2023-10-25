import tkinter as tk
from tkinter import messagebox, INSERT
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    passw = pass_text.get('1.0', 'end-1c')
    if len(passw) != 0:
        pass_text.delete('1.0', 'end')

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)
    password = "".join(password_list)
    pass_text.insert(INSERT, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def clearTextInput():
    web_text.delete('1.0', 'end')
    mail_text.delete('1.0', 'end')
    pass_text.delete('1.0', 'end')


def retrieve_input():
    web = web_text.get('1.0', 'end-1c')
    mail = mail_text.get('1.0', 'end-1c')
    passw = pass_text.get('1.0', 'end-1c')
    new_data = {
        web: {
            "email": mail,
            "password": passw
        }
    }

    if len(web) == 0 or len(mail) == 0 or len(passw) == 0:
        messagebox.showwarning(title="Oops!", message="You cannot leave fields Empty!!!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            clearTextInput()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    web = web_text.get('1.0', 'end-1c')
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title=web, message="No Data file Found")
    else:
        if web in data:
            email = data[web]["email"]
            password = data[web]["password"]
            messagebox.showinfo(title=web, message=f"email/Username: {email}\n Password: {password}.")
            pyperclip.copy(password)
        else:
            messagebox.showwarning(title="Error", message=f"no details for {web} exists.")


# ---------------------------- UI SETUP ------------------------------- #
root = tk.Tk()
root.title("Password Manager")
root.config(padx=50, pady=50)
canvas = tk.Canvas(height=200, width=200)
myImg = tk.PhotoImage(file='logo.png')

canvas.create_image(100, 100, image=myImg, anchor="center")
canvas.grid(row=0, column=1)
# Labels
web_label = tk.Label(text='Website :')
email_label = tk.Label(text='Email/Username :')
password_label = tk.Label(text='Password :')
web_label.grid(row=1, column=0)
email_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)
# textbox
web_text = tk.Text(height=1, width=21)
web_text.grid(row=1, column=1)
web_text.focus_set()

mail_text = tk.Text(height=1, width=35)
mail_text.grid(row=2, column=1, columnspan=2)

pass_text = tk.Text(height=1, width=21)
pass_text.grid(row=3, column=1)
# button
gen_but = tk.Button(text='Generate Password', command=lambda: gen_pass())
gen_but.grid(row=3, column=2, pady=3)

add_but = tk.Button(text='Add', width=20, command=lambda: retrieve_input())
add_but.grid(row=4, column=1, pady=3)

search_but = tk.Button(text='Search', width=15, command=lambda: find_password())
search_but.grid(row=1, column=2, pady=3)
root.mainloop()
