import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Chess with quests v0.1")
window.geometry("1000x500")


title_label = ttk.Label(master = window, text = "Chess with quest", font = "Calibri 24 bold")
title_label.pack()

input_frame = tk.Frame(master = window)
entry = ttk.Entry(master = input_frame, width = 50, font = ("Calibri", 12))

#run
window.mainloop()
