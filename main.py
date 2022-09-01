from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    passwd_ent.insert(0, password)
    try:
        pyperclip.copy(password)
    except pyperclip.PyperclipException:
        pass


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_password():
    website = website_ent.get()
    email = email_ent.get()
    password = passwd_ent.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if (website == "") or (password == ""):
        messagebox.showinfo(title="Oops", message="Please fill all fields")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\n"
                                                              f"Password: {password}")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_ent.delete(0, END)
                email_ent.delete(0, END)
                email_ent.insert(0, "mail@gmail.com")
                passwd_ent.delete(0, END)


# ------------------------------Find Password --------------------------------#
def find_password():
    website = website_ent.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email : {email}\n"
                                                       f"Password : {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for the {website} exists")


# ---------------------------- UI SETUP -------------------------------------- #


# root window
root = Tk()
root.title("Password Manager")
root.config(padx=50, pady=50)

# lock canvas
lock_logo = PhotoImage(file='logo.png')
canvas = Canvas(root, width=200, height=200)
canvas.create_image(100, 100, image=lock_logo)
canvas.grid(row=1, column=2)

# website row
website_lb = Label(root, text="Website:")
website_lb.grid(row=2, column=1)
website_ent = Entry(width=26)
website_ent.grid(row=2, column=2)
website_ent.focus()
search_btn = Button(text="Search", width=16, command=find_password)
search_btn.grid(row=2, column=3)

# email row
email_lb = Label(text="Email/Username:")
email_lb.grid(row=3, column=1)
email_ent = Entry(width=46)
email_ent.grid(row=3, column=2, columnspan=2)
email_ent.insert(0, "mail@gmail.com")

# passwd row
passwd_lb = Label(text="Password:")
passwd_lb.grid(row=4, column=1)
passwd_ent = Entry(width=26)
passwd_ent.grid(row=4, column=2)
gen_passwd_btn = Button(text="Generate Password", command=generate_password)
gen_passwd_btn.grid(row=4, column=3)

# add btn row
add_btn = Button(text="Add", width=43, command=add_password)
add_btn.grid(row=5, column=2, columnspan=2)
root.mainloop()
