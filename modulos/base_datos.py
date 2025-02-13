import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox

def conectar_bd(nombre_bd):
    """Conecta a una base de datos SQLite."""
    return sqlite3.connect(nombre_bd)

# modulos/base_datos.py
def seleccionar_bd():
    # Abrir un cuadro de diálogo para seleccionar la base de datos
    ruta_bd = filedialog.askopenfilename(
        title="Seleccionar base de datos",
        filetypes=[("Archivos SQLite", "*.db")]
    )
    
    if ruta_bd:
        return ruta_bd  # Retorna la ruta de la base de datos seleccionada
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna base de datos.")
        return None
    

def ejecutar_consulta(sentencia_sql, nombre_bd):
    """Ejecuta una consulta SQL en la base de datos."""
    conexion = conectar_bd(nombre_bd)
    cursor = conexion.cursor()
    cursor.execute(sentencia_sql)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def cargar_csv_a_bd(ruta_csv, nombre_bd, nombre_tabla):
    try:
        # Intenta cargar el archivo CSV con un encoding específico
        df = pd.read_csv(ruta_csv, encoding="ISO-8859-1")  # Prueba con ISO-8859-1
        print("CSV cargado correctamente")

        # El resto de la función sigue igual para insertar los datos en la base de datos
        # ...
    except Exception as e:
        print(f"Error al cargar el CSV: {e}")


def obtener_columnas(nombre_bd, nombre_tabla):
    try:
        with sqlite3.connect(nombre_bd) as conn:
            cursor = conn.cursor()
            # Asegúrate de envolver el nombre de la tabla entre comillas
            cursor.execute("PRAGMA table_info(?)", (nombre_tabla,))
            columnas = cursor.fetchall()
            return [columna[1] for columna in columnas]
    except sqlite3.Error as e:
        print(f"Error al obtener columnas: {e}")
        return []
    
def obtener_tablas_bd(nombre_bd):
    """Obtiene el nombre de las tablas en la base de datos SQLite."""
    with sqlite3.connect(nombre_bd) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
    return [tabla[0] for tabla in tablas] 
