import tkinter as tk
from tkinter import ttk

def inicializar_treeview(parent, columnas):
    treeview = ttk.Treeview(parent, columns=columnas, show='headings')
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=150, anchor='center')
    treeview.pack(expand=True, fill='both')
    return treeview 

def limpiar_treeview(treeview):
    for item in treeview.get_children():
        treeview.delete(item)
