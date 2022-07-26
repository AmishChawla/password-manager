from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
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

    password_letters = [random.choice(letters) for _ in range(nr_letters)]

    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
            messagebox.showinfo(title=website,
                                message=f"Username: {data[website]['email']}\n\nPassword: {data[website]['password']}")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Sorry, no websites are stored!")
    except KeyError:
        messagebox.showerror(title="Error", message=f"You don't have {website} saved!")



def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Empty fields", message="Some feilds are empty.")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\n"
                                               f"Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", mode="r") as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
# ------------------------------canvas----------------------------------------------------#
logo = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(row=1, column=2)
# -------------------------------labels--------------------------------------------------------#
website_label = Label(text="Website:", font=("Arial", 12))
website_label.grid(row=2, column=1)
email_label = Label(text="Email/Username:", font=("Arial", 12))
email_label.grid(row=3, column=1)
password_label = Label(text="Password:", font=("Arial", 12))
password_label.grid(row=4, column=1)
# --------------------------------entries-----------------------------------------------------------#
website_entry = Entry(width=17)
website_entry.grid(row=2, column=2, sticky="EW", pady=5, ipady=3)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=3, column=2, columnspan=2, sticky="EW", pady=5, ipady=3)

password_entry = Entry(width=17)
password_entry.grid(row=4, column=2, sticky="EW", pady=5, ipady=3)

# -----------------------------------buttons------------------------------------------------------------#
search_button = Button(text="Search", highlightthickness=0, bd=1, command=find_password)
search_button.grid(row=2, column=3, sticky="EW", pady=5, padx=5, ipady=3)
generate_button = Button(text="Generate Password", highlightthickness=0, bd=1, command=generate_password)
generate_button.grid(row=4, column=3, sticky="EW", pady=5, padx=5, ipady=3)
add_button = Button(text="Add", width=30, highlightthickness=0, bd=1, command=save_password)
add_button.grid(row=5, column=2, columnspan=2, sticky="EW", pady=5, padx=5, ipady=3)

window.mainloop()
