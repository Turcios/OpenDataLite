import csv
import sqlite3
import tkinter as tk
from tkinter import END, filedialog, messagebox
import modulos.variable as var
from modulos.idioma import obtener_texto  # Asegúrate de importar esto

def conectar_bd(nombre_bd):
    return sqlite3.connect(nombre_bd)

def seleccionar_bd():
    ruta_bd = filedialog.askopenfilename(
        title=obtener_texto("select_db_title"),
        filetypes=[("Archivos SQLite", "*.db")]
    )
    
    if ruta_bd:
        return ruta_bd
    else:
        messagebox.showwarning(obtener_texto("warning_title"), obtener_texto("warning_no_db_selected"))
        return None

def ejecutar_consulta(sentencia_sql, nombre_bd):
    try:
        with sqlite3.connect(nombre_bd) as conexion:
            cursor = conexion.cursor()
            cursor.execute(sentencia_sql)
            columnas = [desc[0] for desc in cursor.description]
            filas = cursor.fetchall()
            return columnas, filas
    except sqlite3.OperationalError as e:
        messagebox.showerror(obtener_texto("sql_error"), f"{obtener_texto('sql_query_error')}:\n{e}")
        return None, None

def mostrar_resultados(treeview, columnas, filas):
    for item in treeview.get_children():
        treeview.delete(item)

    if not columnas:
        return

    treeview["columns"] = ["Indice"] + columnas
    treeview["show"] = "headings"
    
    treeview.heading("Indice", text=obtener_texto("index"))
    treeview.column("Indice", width=40, anchor='center')
    
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=150, anchor='center')

    for idx, fila in enumerate(filas, start=1):
        treeview.insert("", "end", values=(idx,) + fila)

    messagebox.showinfo(obtener_texto("success"), obtener_texto("query_success"))

def ejecutar_sql(query_entry, treeview, nombre_bd, root, ruta_archivo):
    sentencia_sql = query_entry.get("1.0", END).strip()
    if not sentencia_sql:
        messagebox.showwarning(obtener_texto("warning_title"), obtener_texto("query_empty"))
        return

    if not nombre_bd:
        messagebox.showerror(obtener_texto("error_title"), obtener_texto("error_no_db"))
        return

    try:
        loading_message = tk.Toplevel(root)
        loading_message.title(obtener_texto("loading_title"))
        loading_message.geometry("300x100")
        
        root.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2 - 150)
        y = root.winfo_y() + (root.winfo_height() // 2 - 50)
        loading_message.geometry(f"300x100+{x}+{y}")
        loading_message.grab_set()
        loading_message.iconbitmap(ruta_archivo)
        loading_message.transient(root)
        loading_message.grab_set()
        
        tk.Label(loading_message, text=obtener_texto("executing_query")).pack(expand=True)
        loading_message.update()
        
        columnas, filas = ejecutar_consulta(sentencia_sql, nombre_bd)

        for item in treeview.get_children():
            treeview.delete(item)

        if columnas and filas:
            treeview["columns"] = ["Índice"] + columnas
            treeview["show"] = "headings"

            treeview.heading("Índice", text=obtener_texto("index"))
            treeview.column("Índice", width=40, anchor='center')

            for col in columnas:
                treeview.heading(col, text=col)
                treeview.column(col, width=150, anchor='center')

            for idx, fila in enumerate(filas, start=1):
                treeview.insert("", "end", values=(idx,) + fila)

            messagebox.showinfo(obtener_texto("success"), obtener_texto("query_success"))
        else:
            messagebox.showinfo(obtener_texto("success"), obtener_texto("no_results"))
    except Exception as e:
        messagebox.showerror(obtener_texto("sql_error"), f"{obtener_texto('sql_query_error')}:\n{e}")
    finally:
        loading_message.destroy()

def validar_bd(self):
    if not hasattr(var, 'nombre_bd') or not var.nombre_bd:
        messagebox.showerror(obtener_texto("error_title"), obtener_texto("error_no_db"))
        return

    query = self.query_entry.get("1.0", tk.END).strip()
    if not query:
        messagebox.showwarning(obtener_texto("warning_title"), obtener_texto("query_empty"))
        return 

    columnas, resultados = ejecutar_consulta(query, var.nombre_bd)
    mostrar_resultados(self, columnas, resultados)

def exportar_consulta(query_entry):
    consulta = query_entry.get("1.0", "end").strip()

    lineas_validas = [
        linea for linea in consulta.splitlines()
        if not linea.strip().startswith('--') and linea.strip() != ''
    ]
    consulta_sin_comentarios = "\n".join(lineas_validas)

    if not consulta_sin_comentarios:
        messagebox.showwarning(obtener_texto("warning_title"), obtener_texto("no_valid_query"))
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".sql",
        filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(consulta_sin_comentarios)
        messagebox.showinfo(obtener_texto("success"), obtener_texto("export_success"))

def exportar_resultados_csv(self):
    columnas = [self.treeview.heading(col)["text"] for col in self.treeview["columns"]]

    filas = []
    for item in self.treeview.get_children():
        fila = self.treeview.item(item)["values"]
        filas.append(fila)

    if not filas:
        messagebox.showwarning(obtener_texto("warning_title"), obtener_texto("no_export_data"))
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"),   ("Text files", "*.txt")])
    if not file_path:
        return

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columnas)
        writer.writerows(filas)

    messagebox.showinfo(obtener_texto("success"), obtener_texto("export_success"))
