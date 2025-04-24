import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
import sqlite3 
import modulos.variable as var
import csv
from modulos.idioma import obtener_texto


# Contexto para almacenar rutas y configuraciones actuales
db_context = {"nombre_bd": None, "nombre_tabla": None,"ruta_csv": None}

# Selección de archivos con un cuadro de diálogo
def seleccionar_archivo(tipo_archivo):
    tipos = {1: ("Archivos SQLite", "*.db"), 2: ("CSV files", "*.csv")}
    ruta_archivo = filedialog.askopenfilename(title=f"Seleccionar {tipos[tipo_archivo][0]}", filetypes=[tipos[tipo_archivo]])
    if ruta_archivo:
        if tipo_archivo == 1:
            var.ruta_bd = ruta_archivo
        else:
            db_context["ruta_csv"] = ruta_archivo
    else:
        messagebox.showwarning("Advertencia", f"No se seleccionó ningún {tipos[tipo_archivo][0].lower()}.")

# Crear una nueva base de datos e importar CSV
def abrir_nueva_ventana(frame_izquierdo):
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("OpenDataLite")
    nueva_ventana.geometry("600x400+300+200")

    nueva_ventana.transient(nueva_ventana.master)  # Hace que la ventana dependa de la principal
    nueva_ventana.grab_set()  # Bloquea la interacción con la ventana principal

    # Componentes de entrada
    entradas = {
        "Nombre de la base de datos": tk.Entry(nueva_ventana),
        "Nombre de la tabla": tk.Entry(nueva_ventana)
    }
    for label_text, entry in entradas.items():
        tk.Label(nueva_ventana, text=label_text).pack(pady=5)
        entry.pack(pady=5)

    # Botón para seleccionar archivo CSV
    tk.Button(nueva_ventana, text="Seleccionar CSV", command=lambda: seleccionar_archivo(2)).pack(pady=5)

    # Botón para confirmar y crear la base de datos
    tk.Button(
        nueva_ventana, text="Enviar",
        command=lambda: mostrar_datos(entradas["Nombre de la base de datos"].get(), entradas["Nombre de la tabla"].get(), frame_izquierdo, nueva_ventana)
    ).pack(pady=10)

# Cargar y mostrar datos desde el CSV a la base de datos nueva
def mostrar_datos(nombre_bd, nombre_tabla, frame_izquierdo, nueva_ventana):
    if not db_context.get("ruta_csv"):
        messagebox.showerror("Error", "No se ha seleccionado un archivo CSV.")
        return

    try:
        df = pd.read_csv(db_context["ruta_csv"], on_bad_lines='skip')
        conexion = sqlite3.connect(nombre_bd + ".db")
           # Detectar automáticamente el delimitador
        with open(db_context["ruta_csv"], 'r', encoding='utf-8') as file:
            sample = file.read(2048)  # Leer una porción del archivo para análisis
            dialect = csv.Sniffer().sniff(sample, delimiters="-,/.\t")  # Incluir los delimitadores permitidos
            file.seek(0)  # Volver al inicio del archivo

        # Cargar el CSV 
        chunksize = 100000  # Ajusta este valor según la memoria disponible
        for chunk in pd.read_csv(db_context["ruta_csv"], delimiter=dialect.delimiter, on_bad_lines='skip', chunksize=chunksize):
            chunk.to_sql(nombre_tabla, conexion, if_exists='append', index=False)
            
        conexion.close()
        messagebox.showinfo("Éxito", "CSV cargado exitosamente.")
        mostrar_estructura(nombre_bd + ".db", frame_izquierdo)
        db_context.update({"nombre_bd": nombre_bd + ".db", "nombre_tabla": nombre_tabla})
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar CSV: {e}")
    finally:
        nueva_ventana.destroy()

# Cargar CSV en una base de datos existente
def cargar_csv_bd(frame_izquierdo, nombre_tabla, ventana_carga):
    try:
        conexion = sqlite3.connect(var.ruta_bd)

        # Detectar automáticamente el delimitador
        with open(db_context["ruta_csv"], 'r', encoding='utf-8') as file:
            sample = file.read(2048)  # Leer una porción del archivo para análisis
            dialect = csv.Sniffer().sniff(sample, delimiters=",/.–\t")  # Incluir los delimitadores permitidos
            file.seek(0)  # Volver al inicio del archivo

        # Cargar el CSV 
        chunksize = 100000  # Ajusta este valor según la memoria disponible
        for chunk in pd.read_csv(db_context["ruta_csv"], delimiter=dialect.delimiter, on_bad_lines='skip', chunksize=chunksize):
            chunk.to_sql(nombre_tabla, conexion, if_exists='append', index=False)

        conexion.close()

        mostrar_estructura(var.ruta_bd, frame_izquierdo)
        messagebox.showinfo("Éxito", "Datos agregados a la base de datos.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar CSV en la base de datos: {e}")
    finally:
        ventana_carga.destroy()

# Ventana para cargar una base de datos existente
def cargar_base(frame_izquierdo, menu):
    archivo = filedialog.askopenfilename(
        title="Seleccionar base de datos SQLite",
        filetypes=[("SQLite files", "*.sqlite *.db"), ("Todos los archivos", "*.*")]
    )
    
    if archivo:
        try:
            var.ruta_bd = archivo  # Asignamos el archivo seleccionado a la variable global
            conexion = sqlite3.connect(var.ruta_bd)
            conexion.close()
            mostrar_estructura(var.ruta_bd, frame_izquierdo)
            menu.entryconfig(obtener_texto('CSV'), state='normal')
            messagebox.showinfo("Éxito", "Base de datos cargada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la base de datos: {e}")

def cargar_csv(frame_izquierdo):
    ventana_carga = tk.Toplevel()
    ventana_carga.title("OpenDataLite")
    ventana_carga.geometry("600x400+300+200")

    ventana_carga.transient(ventana_carga.master)  # Hace que la ventana dependa de la principal
    ventana_carga.grab_set()   # Bloquea la interacción con la ventana principal

    # Componentes para seleccionar tabla
    tk.Button(ventana_carga, text="Seleccionar CSV", command=lambda: seleccionar_archivo(2)).pack(pady=5)

    label_nombre_tabla = tk.Label(ventana_carga, text="Nombre de la tabla")
    label_nombre_tabla.pack(pady=5)
    entry_nombre_tabla = tk.Entry(ventana_carga)
    entry_nombre_tabla.pack(pady=5)

    tk.Button(
        ventana_carga, text="Enviar",
        command=lambda: cargar_csv_bd(frame_izquierdo, entry_nombre_tabla.get(), ventana_carga)
    ).pack(pady=10)

# Mostrar estructura de la base de datos en un Treeview
def mostrar_estructura(nombre_bd, frame_izquierdo):
    for widget in frame_izquierdo.winfo_children():
        widget.destroy()

    tk.Label(frame_izquierdo, text=f"Estructura: {nombre_bd}").pack(pady=5)

    treeview = ttk.Treeview(frame_izquierdo)
    treeview.pack(expand=True, fill="both", padx=10, pady=10)
    treeview.heading("#0", text="Tablas", anchor="w")

    try:
        var.nombre_bd =  f'{nombre_bd}'
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for tabla in cursor.fetchall():
            nombre_tabla = tabla[0]
            nodo_tabla = treeview.insert("", "end", text=nombre_tabla, open=False)
            cursor.execute(f"PRAGMA table_info('{nombre_tabla}');")
            for columna in cursor.fetchall():
                treeview.insert(nodo_tabla, "end", text=columna[1], open=False)
    finally:
        conexion.close()

# Función principal para determinar tipo de operación
def nueva_archivo(frame_izquierdo, tipo):
    if tipo == 1:
        cargar_csv(frame_izquierdo)
    elif tipo == 2:
        abrir_nueva_ventana(frame_izquierdo)
         
