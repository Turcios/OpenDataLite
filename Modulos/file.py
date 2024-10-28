import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
import sqlite3

# Variables globales para almacenar la base de datos y tabla cargadas
db_context = {"nombre_bd": None, "nombre_tabla": None}

# Función para abrir una nueva ventana después de cargar el archivo
def abrir_nueva_ventana(file_path, frame_izquierdo):
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("OpenDataLite")

     # Definir el tamaño de la nueva ventana
    ancho_ventana = 600
    alto_ventana = 400
    x_ventana = int((850 / 2) - (ancho_ventana / 2))
    y_ventana = int((400 / 2) - (alto_ventana / 2))

     # Establecer la geometría de la ventana nueva
    nueva_ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

     # Etiqueta de campo del nombre de la base de datos
    label_nombre_bd = tk.Label(nueva_ventana, text="Nombre base de datos:")
    label_nombre_bd.pack(pady=5)

    # Entrada de texto para el nombre
    entry_nombre_bd = tk.Entry(nueva_ventana)
    entry_nombre_bd.pack(pady=5)

    # Etiqueta de campo del nombre de la tabla
    label_nombre_tabla = tk.Label(nueva_ventana, text="Nombre de la tabla")
    label_nombre_tabla.pack(pady=5)

    # Entrada de texto para el nombre
    entry_nombre_tabla = tk.Entry(nueva_ventana)
    entry_nombre_tabla.pack(pady=5)    

    boton_enviar = tk.Button(
        nueva_ventana, 
        text="Enviar", 
        command=lambda: mostrar_datos(entry_nombre_bd.get(), entry_nombre_tabla.get(), file_path, frame_izquierdo, nueva_ventana)
    )
    boton_enviar.pack(pady=10)

# Función para mostrar los datos ingresados en el formulario
def mostrar_datos(nombre_bd, nombre_tabla, file_path, frame_izquierdo, nueva_ventana):
    if file_path:
        try:
            df = pd.read_csv(file_path, on_bad_lines='skip')  # Permite saltar líneas problemáticas

            conexion = sqlite3.connect(nombre_bd + ".db")
            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
            conexion.close()

            messagebox.showinfo("Éxito", "El archivo CSV ha sido cargado en la base de datos correctamente.")
            mostrar_estructura(nombre_bd + ".db", frame_izquierdo)

            # Guardar el contexto actual de la base de datos y la tabla
            db_context["nombre_bd"] = nombre_bd + ".db"
            db_context["nombre_tabla"] = nombre_tabla

        except pd.errors.ParserError as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: formato incorrecto en alguna línea.\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    nueva_ventana.destroy()

# Obtener el contexto actual para poder hacer las consultas con la bd que se cargo
def obtener_contexto():
    return db_context

def nueva_archivo(frame_izquierdo):
    file_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("CSV files", "*.csv")])
    if file_path:
        abrir_nueva_ventana(file_path, frame_izquierdo)
    else:
        print("No se seleccionó ningún archivo.")


 # Función para mostrar la estructura de la base de datos en una nueva ventana
def mostrar_estructura(nombre_bd, frame_izquierdo):
    # Limpiar el frame izquierdo antes de cargar la nueva estructura
    for widget in frame_izquierdo.winfo_children():
        widget.destroy()

 # Crear una etiqueta de título en el frame izquierdo
    label_estructura = tk.Label(frame_izquierdo, text=f"Estructura: {nombre_bd}")
    label_estructura.pack(pady=5)

# Crear un Treeview para mostrar la estructura de la base de datos
    treeview = ttk.Treeview(frame_izquierdo)
    treeview.pack(expand=True, fill="both", padx=10, pady=10)

    # Crear la columna principal del Treeview
    treeview.heading("#0", text="Tablas", anchor="w")

 # Conectar a la base de datos y obtener la información de las tablas
    conexion = sqlite3.connect(nombre_bd)
    cursor = conexion.cursor()

    # Obtener la lista de tabla
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    
     # Recorrer las tablas y obtener sus columnas
    for tabla in tablas:
        nombre_tabla = tabla[0]
        nodo_tabla = treeview.insert("", "end", text=nombre_tabla, open=False)

        # Obtener las columnas de cada tabla
        cursor.execute(f"PRAGMA table_info({nombre_tabla});")
        columnas = cursor.fetchall()

        # Insertar las columnas como nodos hijos
        for columna in columnas:
            treeview.insert(nodo_tabla, "end", text=columna[1], open=False)

        # Cerrar la conexión
    conexion.close()