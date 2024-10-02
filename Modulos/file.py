import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
import sqlite3

# Función para abrir una nueva ventana después de cargar el archivo
def abrir_nueva_ventana(file_path):
    nueva_ventana = tk.Toplevel();
    # Crear nueva ventana
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

    # Etiqueta para mostrar el contenido del archivo
    label_contenido = tk.Label(nueva_ventana, text="Contenido del archivo:")
    label_contenido.pack(pady=10)

    # Botón de enviar
    boton_enviar = tk.Button(nueva_ventana, text="Enviar", command=lambda: mostrar_datos(entry_nombre_bd.get(), entry_nombre_tabla.get(), file_path, nueva_ventana))
    boton_enviar.pack(pady=10)

# Función para mostrar los datos ingresados en el formulario
def mostrar_datos(nombre_bd,nombre_tabla,file_path,nueva_ventana):
    if file_path:
        try:
            # Leer el CSV con pandas
            df = pd.read_csv(file_path)
            
            # Conectar a la base de datos SQLite (se crea si no existe)
            conexion = sqlite3.connect(nombre_bd+".db")
            
            # Insertar el DataFrame en una tabla de SQLite
            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
            
            # Cerrar la conexión
            conexion.close()
            
            # Mostrar un mensaje de éxito
            messagebox.showinfo("Éxito", "El archivo CSV ha sido cargado en la base de datos correctamente.")

            # Mostrar la estructura de la tabla
            mostrar_estructura(nombre_bd+".db")

        except Exception as e:
            # Mostrar un mensaje de error si algo falla
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    #cierra la ventana al enviar los datos
    nueva_ventana.destroy()
    
def nueva_archivo():
    file_path = filedialog.askopenfilename(
    title="Seleccionar archivo CSV",
    filetypes=[("CSV files", "*.csv")]  # Limita a solo archivos CSV
    )
    # Verificar si se seleccionó un archivo
    if file_path:
        # Abrir y leer el archivo CSV
        with open(file_path, 'r') as file:
            content = file.read()
            print("Contenido del archivo CSV:")
            print(content)
            abrir_nueva_ventana(file_path)  # Llamar a la función para abrir la nueva ventana
    else:
        print("No se seleccionó ningún archivo.")


    # Función para mostrar la estructura de la base de datos en una nueva ventana
def mostrar_estructura(nombre_bd):
    # Crear una nueva ventana para mostrar la estructura
    ventana_estructura = tk.Toplevel()
    ventana_estructura.title(f"Estructura de la Base de Datos: {nombre_bd}")
    ventana_estructura.geometry("600x400")
    
    # Crear un Treeview para mostrar la estructura de la base de datos
    treeview = ttk.Treeview(ventana_estructura)
    treeview.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Crear la columna principal del Treeview
    treeview.heading("#0", text=nombre_bd[:-3], anchor="w")

    # Conectar a la base de datos y obtener la información de las tablas
    conexion = sqlite3.connect(nombre_bd)
    cursor = conexion.cursor()
    
    # Obtener la lista de tablas
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