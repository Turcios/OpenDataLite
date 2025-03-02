import sqlite3
import tkinter as tk
from tkinter import END, filedialog, messagebox
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
    
def mostrar_resultados(self, columnas, resultados):
    """Muestra los resultados en el Treeview ocupando todo el espacio disponible."""

    # Ocultar el cuadro de texto de resultados si hay datos
    self.result_text.pack_forget()

    # Si no hay resultados, mostrar un mensaje en `self.result_text`
    if not resultados:
        self.result_text.pack(fill='both', expand=True)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "No se encontraron resultados.")
        return

    # Si `Treeview` ya existe, limpiar y reutilizar
    if hasattr(self, 'treeview'):
        self.treeview.delete(*self.treeview.get_children())
        self.treeview["columns"] = columnas
    else:
        # Crear el Treeview si no existe
        self.treeview = tk.Treeview(self.frame_treeview, columns=columnas, show="headings")

        # Barra de desplazamiento
        self.scrollbar = tk.Scrollbar(self.frame_treeview, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscroll=self.scrollbar.set)

        # Ubicar Treeview y Scrollbar en la cuadrícula
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar expansión en el frame contenedor
        self.frame_treeview.grid_rowconfigure(0, weight=1)
        self.frame_treeview.grid_columnconfigure(0, weight=1)

    # Configurar encabezados y tamaño automático
    for col in columnas:
        self.treeview.heading(col, text=col)
        self.treeview.column(col, anchor="center", stretch=True, width=150)  # Ajusta el tamaño automáticamente

    # Insertar los datos en la tabla
    for fila in resultados:
        self.treeview.insert("", "end", values=fila)

def ejecutar_consulta(query, db_path):
    """Ejecuta la consulta SQL y devuelve los resultados."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        columnas = [desc[0] for desc in cursor.description]  # Obtiene los nombres de las columnas
        resultados = cursor.fetchall()
        conn.close()
        return columnas, resultados
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar la consulta: {str(e)}")
        return [], []

    
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
