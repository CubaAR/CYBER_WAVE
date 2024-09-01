import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
    cursor.execute("SELECT * FROM users")
    db.commit()
class GUI:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()

        master.title('Password Generator')
        master.geometry('660x500')
        master.config(bg='#F8F8FF')
        master.resizable(False, False)

        Label(master, text="PASSWORD GENERATOR", anchor=N, fg='darkblue',font='arial 20 bold').grid(row=0, column=0, columnspan=2, pady=(10, 20))

        Label(master, text="Enter User Name:", font='times 15 bold', fg='darkblue').grid(row=1, column=0,padx=10, pady=5,sticky=E)

        self.textfield = Entry(master, textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        self.textfield.focus_set()

        Label(master, text="Enter Password Length:", font='times 15 bold', fg='darkblue').grid(row=2,column=0,padx=10,pady=5,sticky=E)

        self.length_textfield = Entry(master, textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        Label(master, text="Generated Password:", font='times 15 bold', fg='darkblue').grid(row=3,column=0,padx=10,pady=5,sticky=E)
        self.generated_password_textfield = Entry(master, textvariable=self.n_generatedpassword, font='times 15', bd=6,relief='ridge')
        self.generated_password_textfield.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        Button(master, text="GENERATE PASSWORD", bd=3, relief='solid', padx=10, pady=5, font='Verdana 15 bold',fg='#68228B', bg='#BCEE68', command=self.generate_pass).grid(row=4, column=0, columnspan=2, pady=10)

        Button(master, text="ACCEPT", bd=3, relief='solid', padx=10, pady=5, font='Helvetica 15 bold italic',fg='#458B00', bg='#FFFAF0', command=self.accept_fields).grid(row=5, column=0, columnspan=2, pady=10)

        Button(master, text="RESET", bd=3, relief='solid', padx=10, pady=5, font='Helvetica 15 bold italic',fg='#458B00', bg='#FFFAF0', command=self.reset_fields).grid(row=6, column=0, columnspan=2, pady=10)

    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"

        upper = list(upper)
        lower = list(lower)
        chars = list(chars)
        numbers = list(numbers)

        name = self.textfield.get()
        leng = self.length_textfield.get()

        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.textfield.delete(0, END)
            return

        try:
            length = int(leng)
        except ValueError:
            messagebox.showerror("Error", "Password length must be a number")
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        self.generated_password_textfield.delete(0, END)

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers,n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.generated_password_textfield.insert(0, gen_passwd)

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = "SELECT * FROM users WHERE Username = ?"
            cursor.execute(find_user, (self.n_username.get(),))

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username.")
            else:
                insert = "INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)"
                cursor.execute(insert, (self.n_username.get(), self.n_generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success!", "Password generated successfully")
    def reset_fields(self):
        self.textfield.delete(0, END)
        self.length_textfield.delete(0, END)
        self.generated_password_textfield.delete(0, END)


if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()
