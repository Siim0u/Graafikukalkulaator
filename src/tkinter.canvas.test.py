from tkinter import *
from tkinter import ttk

window = Tk()

window.title("Graafikukalkulaator")

window.geometry("800x600")

def temp_text(e):
   x_algus.delete(0,"end")

x_algus = ttk.Entry(window)
x_algus.place(x=50, y=450, width=100, height=30)
x_algus.insert(0, "This is Temporary Text...")
x_algus.bind("<FocusIn>", temp_text)

x_lõpp = ttk.Entry(window)
x_lõpp.place(x=250, y=450, width=100, height=30)

y_algus = ttk.Entry(window)
y_algus.place(x=450, y=450, width=100, height=30)

y_lõpp = ttk.Entry(window)
y_lõpp.place(x=650, y=450, width=100, height=30)

