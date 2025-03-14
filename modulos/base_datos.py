import sqlite3
import tkinter as tk
from tkinter import END, filedialog, messagebox
from tkinter.ttk import Treeview
import modulos.variable as var


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
    """Ejecuta una consulta SQL en la base de datos seleccionada y devuelve los resultados."""
    try:
        with sqlite3.connect(nombre_bd) as conexion:
            cursor = conexion.cursor()
            cursor.execute(sentencia_sql)
            columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
            filas = cursor.fetchall()  # Obtener todas las filas de la consulta
            return columnas, filas
    except sqlite3.OperationalError as e:
        messagebox.showerror("Error de SQL", f"Error en la consulta SQL:\n{e}")
        return None, None


def mostrar_resultados(treeview, columnas, filas):
    """Muestra los resultados de una consulta SQL en un Treeview."""
    # Limpiar el Treeview antes de poblarlo con nuevos datos
    for item in treeview.get_children():
        treeview.delete(item)

    if not columnas:
        return  # No hay resultados

    # Configurar las columnas del Treeview
    treeview["columns"] = ["Indice"] + columnas  # Añadir columna para el índice
    treeview["show"] = "headings"  # Mostrar encabezados de columnas
    
    # Configurar encabezados de columna en el Treeview
    treeview.heading("Indice", text="Índice")  # Encabezado para el índice
    treeview.column("Indice", width=40, anchor='center')  # Ajuste de ancho para el índice
    
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=150, anchor='center')  # Ajuste de ancho para cada columna

    # Insertar filas en el Treeview con índice
    for idx, fila in enumerate(filas, start=1):
        treeview.insert("", "end", values=(idx,) + fila)  # Insertar índice + fila

    # Muestra un mensaje de éxito
    messagebox.showinfo("Éxito", "Consulta ejecutada exitosamente.")


def ejecutar_sql(query_entry, treeview, result_text, nombre_bd):
    """Ejecuta la consulta SQL y muestra los resultados en result_text y en el Treeview."""
    sentencia_sql = query_entry.get("1.0", END).strip()
    if not sentencia_sql:
        messagebox.showwarning("Entrada vacía", "Por favor ingresa una sentencia SQL.")
        return

    if not nombre_bd:
        messagebox.showerror("Error", "No hay una base de datos cargada actualmente.")
        return

    try:
        columnas, filas = ejecutar_consulta(sentencia_sql, nombre_bd)

        # Limpiar antes de mostrar nuevos resultados
        result_text.delete("1.0", END)
        for item in treeview.get_children():
            treeview.delete(item)

        if columnas and filas:
            # Mostrar en result_text
            resultados_str = " | ".join(columnas) + "\n"
            resultados_str += "-" * (len(resultados_str) + 5) + "\n"
            resultados_str += "\n".join(" | ".join(map(str, fila)) for fila in filas)
            result_text.insert(END, resultados_str)

            # Mostrar en Treeview
            treeview["columns"] = ["Índice"] + columnas
            treeview["show"] = "headings"

            treeview.heading("Índice", text="Índice")
            treeview.column("Índice", width=40, anchor='center')

            for col in columnas:
                treeview.heading(col, text=col)
                treeview.column(col, width=150, anchor='center')

            for idx, fila in enumerate(filas, start=1):
                treeview.insert("", "end", values=(idx,) + fila)

            messagebox.showinfo("Éxito", "Consulta ejecutada exitosamente.")
        else:
            result_text.insert(END, "No se encontraron resultados para la consulta.")
    except Exception as e:
        result_text.delete("1.0", END)
        result_text.insert(END, f"Error en la consulta SQL:\n{e}")
        messagebox.showerror("Error de SQL", f"Error en la consulta SQL:\n{e}")

   

    # Ejecutar la consulta y obtener los resultados
    #columnas, filas = ejecutar_consulta(sentencia_sql, nombre_bd)
    
    # Mostrar los resultados en el Treeview
    #mostrar_resultados(Treeview, columnas, filas)
    
def validar_bd(self):
    """Ejecuta la consulta y muestra los resultados en una tabla en lugar del cuadro de texto."""
    if not hasattr(var, 'nombre_bd') or not var.nombre_bd:
        messagebox.showerror("Error", "No hay una base de datos cargada")
        return

    query = self.query_entry.get("1.0", tk.END).strip()
    if not query:
        messagebox.showwarning("Advertencia", "La consulta SQL está vacía")
        return 

    columnas, resultados = ejecutar_consulta(query, var.nombre_bd)
    
    mostrar_resultados(self, columnas, resultados)
