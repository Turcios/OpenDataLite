import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
import sqlite3
#import os
import variable

# Variables globales 
db_context = {"nombre_bd": None, "nombre_tabla": None, "ruta_bd":None, "ruta_csv":None}

# Función para seleccionar un archivo SQLite y cargar las tablas en un combobox
def seleccionar_archivo_bd(tipo):
    if tipo==1:
        ruta_bd = filedialog.askopenfilename(title=variable.idioma_actual["seleccionar_archivo_bd"], filetypes=[("Archivos SQLite", "*.db")])
        if ruta_bd:
            db_context["ruta_db"] =ruta_bd
        else:
            db_context["ruta_db"] =variable.idioma_actual["no_seleccion_archivo"]
    else:
        ruta_bd = filedialog.askopenfilename(title=variable.idioma_actual["seleccionar_csv"], filetypes=[("CSV files", "*.csv")])
        if ruta_bd:
            db_context["ruta_csv"] =ruta_bd
        else:
            db_context["ruta_csv"] =variable.idioma_actual["no_seleccion_archivo"]

# Función para abrir una nueva ventana después de cargar el archivo, base de datos nueva
def abrir_nueva_ventana(frame_izquierdo):
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
    label_nombre_bd = tk.Label(nueva_ventana, text=variable.idioma_actual["nombre_base_datos"])
    label_nombre_bd.pack(pady=5)
   
    # Entrada de texto para el nombre
    entry_nombre_bd = tk.Entry(nueva_ventana)
    entry_nombre_bd.pack(pady=5)

    # Etiqueta de campo del nombre de la tabla
    label_nombre_tabla = tk.Label(nueva_ventana, text=variable.idioma_actual["nombre_tabla"])
    label_nombre_tabla.pack(pady=5)

    # Entrada de texto para el nombre
    entry_nombre_tabla = tk.Entry(nueva_ventana)
    entry_nombre_tabla.pack(pady=5)  

    # Etiqueta para seleccionar el archivo de CSV
    label_nombre_bd = tk.Label(nueva_ventana, text=variable.idioma_actual["base_archivo_csv"]+":") 
    label_nombre_bd.pack(pady=5)
    boton_seleccionar_bd = tk.Button(nueva_ventana, text=variable.idioma_actual["seleccionar_csv"], command=lambda: seleccionar_archivo_bd(2))
    boton_seleccionar_bd.pack(pady=5)  

    boton_enviar = tk.Button(
        nueva_ventana, 
        text=variable.idioma_actual[variable.idioma_actual["enviar"]], 
        command=lambda: mostrar_datos(entry_nombre_bd.get(), entry_nombre_tabla.get(), frame_izquierdo, nueva_ventana)
    )
    boton_enviar.pack(pady=10)

# Función para mostrar los datos ingresados en el formulario
def mostrar_datos(nombre_bd, nombre_tabla, frame_izquierdo, nueva_ventana):
    if db_context["ruta_csv"]:
        try:
            df = pd.read_csv(db_context["ruta_csv"], on_bad_lines='skip')  # Permite saltar líneas problemáticas

            conexion = sqlite3.connect(nombre_bd + ".db")
            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
            conexion.close()

            messagebox.showinfo(variable.idioma_actual["exito"], variable.idioma_actual["mensaje_exito_csv"])
            mostrar_estructura(nombre_bd + ".db", frame_izquierdo)

            # Guardar el contexto actual de la base de datos y la tabla
            db_context["nombre_bd"] = nombre_bd + ".db"
            db_context["nombre_tabla"] = nombre_tabla

        except pd.errors.ParserError as e:
            messagebox.showerror("Error", f"{variable.idioma_actual["mensaje_error_carga_linea"]}.\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"{variable.idioma_actual["mensaje_error_carga"]}: {e}")

    nueva_ventana.destroy()

# Obtener el contexto actual para poder hacer las consultas con la bd que se cargo
def obtener_contexto():
    return db_context

#Carga una base de datos existente
def cargar_csv_bd(frame_izquierdo, nombre_tabla,ventana_carga):
    conexion = sqlite3.connect(db_context["ruta_db"])
    print("Conexión exitosa a la base de datos")
    
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(db_context["ruta_csv"], on_bad_lines='skip')
    df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
    print("Datos agregados a la tabla en la base de datos")
    conexion.close()
    mostrar_estructura(db_context["ruta_db"], frame_izquierdo)
    ventana_carga.destroy()

#Carga una base de datos existente
def cargar_base(frame_izquierdo):
    ventana_carga = tk.Toplevel()
    ventana_carga.title("OpenDataLite")

     # Definir el tamaño de la nueva ventana
    ancho_ventana = 600
    alto_ventana = 400
    x_ventana = int((850 / 2) - (ancho_ventana / 2))
    y_ventana = int((400 / 2) - (alto_ventana / 2))

     # Establecer la geometría de la ventana nueva
    ventana_carga.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

     # Etiqueta para seleccionar el archivo de la base de datos
    label_nombre_bd = tk.Label(ventana_carga, text=variable.idioma_actual["base_datos"] )
    label_nombre_bd.pack(pady=5)
    boton_seleccionar_bd = tk.Button(ventana_carga, text=variable.idioma_actual["seleccionar_db"], command=lambda: seleccionar_archivo_bd(1))
    boton_seleccionar_bd.pack(pady=5)  

  # Etiqueta para seleccionar el archivo de la base de datos
    label_nombre_bd = tk.Label(ventana_carga, text=variable.idioma_actual["seleccionar_db"])
    label_nombre_bd.pack(pady=5)
    boton_seleccionar_bd = tk.Button(ventana_carga, text=variable.idioma_actual["seleccionar_csv"], command=lambda: seleccionar_archivo_bd(2))
    boton_seleccionar_bd.pack(pady=5)  

    # Etiqueta de campo del nombre de la tabla
    label_nombre_tabla = tk.Label(ventana_carga, text=variable.idioma_actual["nombre_tabla"])
    label_nombre_tabla.pack(pady=5)

    # Entrada de texto para el nombre
    entry_nombre_tabla = tk.Entry(ventana_carga)
    entry_nombre_tabla.pack(pady=5)    
 # Conectar a la base de datos
   
    boton_enviar = tk.Button(
        ventana_carga, 
        text=variable.idioma_actual["enviar"], 
        command=lambda:cargar_csv_bd(frame_izquierdo,entry_nombre_tabla.get(),ventana_carga)
    )
    boton_enviar.pack(pady=10)
   
def nueva_archivo(frame_izquierdo, tipo):
    print(tipo)
    if tipo == 1:
        cargar_base(frame_izquierdo)
    else:
       abrir_nueva_ventana(frame_izquierdo)

 # Función para mostrar la estructura de la base de datos en una nueva ventana
def mostrar_estructura(nombre_bd, frame_izquierdo):
    # Limpiar el frame izquierdo antes de cargar la nueva estructura
    for widget in frame_izquierdo.winfo_children():
        widget.destroy()

 # Crear una etiqueta de título en el frame izquierdo
    label_estructura = tk.Label(frame_izquierdo, text=f"{variable.idioma_actual['estructura']}: {nombre_bd}" )
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