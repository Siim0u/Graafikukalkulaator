from tkinter import *
from tkinter import ttk

window = Tk()

window.title("Graafikukalkulaator")

window.geometry("800x600")

def temp_x_algus(e):
    x_algus.delete(0,"end")
    
def temp_x_lõpp(e):
    x_lõpp.delete(0,"end")
   
def temp_y_algus(e):
    y_algus.delete(0,"end")

def temp_y_lõpp(e):
    y_lõpp.delete(0,"end")
        
x_algus = ttk.Entry(window)
x_algus.place(x=50, y=450, width=100, height=30)
x_algus.insert(0, "x telje algus")
x_algus.bind("<FocusIn>", temp_x_algus)

x_lõpp = ttk.Entry(window)
x_lõpp.place(x=250, y=450, width=100, height=30)
x_lõpp.insert(0, "x telje lõpp")
x_lõpp.bind("<FocusIn>", temp_x_lõpp)

y_algus = ttk.Entry(window)
y_algus.place(x=450, y=450, width=100, height=30)
y_algus.insert(0, "y telje algus")
y_algus.bind("<FocusIn>", temp_y_algus)


y_lõpp = ttk.Entry(window)
y_lõpp.place(x=650, y=450, width=100, height=30)
y_lõpp.insert(0, "y telje lõpp")
y_lõpp.bind("<FocusIn>", temp_y_lõpp)

canvas=Canvas(window, width=500, height=300)
canvas.pack()
