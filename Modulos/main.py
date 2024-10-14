import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog, ttk
import file  # Asegúrate que el archivo se llame "file.py"

def salir_app():
    root.quit()

def acerca_de():
    messagebox.showinfo("Acerca de", "V1 OpenDataLite")

# Crear la ventana principal
root = tk.Tk()
root.title("OpenDataLite")
root.geometry("850x400")

# Crear el contenedor principal usando "pack" para tener dos columnas
contenedor = tk.Frame(root)
contenedor.pack(fill="both", expand=True)

# Crear el Frame izquierdo para la estructura de la base de datos
frame_izquierdo = tk.Frame(contenedor, width=200)
frame_izquierdo.pack(side="left", fill="both", expand=True)

# Crear el Frame derecho para mostrar otros datos
frame_derecho = tk.Frame(contenedor, width=50)
frame_derecho.pack(side="right", fill="both", expand=True)

# Crear una etiqueta temporal en el frame izquierdo (será reemplazada con la estructura)
label_izquierda = tk.Label(frame_izquierdo, text="Estructura")
label_izquierda.pack(pady=10)

# Crear una etiqueta temporal en el frame derecho para otros datos
label_derecha = tk.Label(frame_derecho, text="Consultas")
label_derecha.pack(pady=10)

# Crear la barra de menú
barra_menu = tk.Menu(root)

# Crear un menú "Archivo"
menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Importar", command=lambda: file.nueva_archivo(frame_izquierdo))
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
