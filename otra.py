import tkinter as tk
from tkinter import messagebox

def nueva_archivo():
    messagebox.showinfo("Importar", "Importar archivo.")

def salir_app():
    root.quit()

def acerca_de():
    messagebox.showinfo("Acerca de", "V1 OpenDataLite")

# Crear la ventana principal
root = tk.Tk()
root.title("OpenDataLite")
root.geometry("850x400")

# Crear la barra de menú
barra_menu = tk.Menu(root)

# Crear un menú "Archivo"
menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Importar", command=nueva_archivo)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir_app)

# Añadir el menú "Archivo" a la barra de menú
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

# Crear un menú "Ayuda"
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)

# Añadir el menú "Ayuda" a la barra de menú
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

# Configurar la ventana para que use la barra de menú
root.config(menu=barra_menu)

# Iniciar el bucle principal de la aplicación
root.mainloop()