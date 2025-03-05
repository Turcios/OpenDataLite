import tkinter as tk
import sqlite3
import pandas as pd
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modulos.graficos import exportar_grafico_pdf
import os
import modulos.variable as var  # Para almacenar la base de datos seleccionada

# Contexto global para almacenar el nombre de la base de datos seleccionada
db_context = {"nombre_bd": None}


def buscar_bases_datos():
    """Busca archivos .db en el directorio actual y devuelve una lista de nombres."""
    carpeta_busqueda = os.getcwd()  # Puedes cambiarlo si deseas otra ruta específica
    return [f for f in os.listdir(carpeta_busqueda) if f.endswith(".db")]

def seleccionar_bd():
    """Permite seleccionar una base de datos existente o cargar una nueva si no hay disponibles."""
    bases_datos = buscar_bases_datos()

    if bases_datos:
        # Si hay bases de datos disponibles, mostrar un Combobox para elegir
        seleccion_bd_window = tk.Toplevel()
        seleccion_bd_window.title("Seleccionar Base de Datos")

        tk.Label(seleccion_bd_window, text="Selecciona una base de datos:").pack(pady=5)
        
        bd_var = tk.StringVar(value=bases_datos[0])  # Selecciona la primera por defecto
        bd_combobox = ttk.Combobox(seleccion_bd_window, textvariable=bd_var, values=bases_datos, state="readonly")
        bd_combobox.pack(pady=5)

        def confirmar_seleccion():
            var.nombre_bd = bd_var.get()  # Guardar la selección en la variable global
            messagebox.showinfo("Base de Datos Seleccionada", f"Usando la base de datos: {var.nombre_bd}")
            seleccion_bd_window.destroy()

        ttk.Button(seleccion_bd_window, text="Confirmar", command=confirmar_seleccion).pack(pady=10)
    
    else:
        # Si no hay bases de datos, pedir que el usuario cargue una nueva
        ruta_bd = filedialog.askopenfilename(title="Seleccionar base de datos", filetypes=[("Archivos SQLite", "*.db")])
        
        if ruta_bd:
            var.nombre_bd = ruta_bd  # Guardar en variable global
            messagebox.showinfo("Base de Datos Seleccionada", f"Base de datos seleccionada: {var.nombre_bd}")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna base de datos.")

def conectar_bd():
    """Conecta a la base de datos seleccionada."""
    if not var.nombre_bd:
        messagebox.showerror("Error", "No hay una base de datos cargada")
        return None
    return sqlite3.connect(var.nombre_bd)


def obtener_datos_bd(nombre_bd, tabla):
    try:
        with sqlite3.connect(nombre_bd) as conn:
            return pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos: {e}")
        return None

def cargar_tablas(tablas_combo):
    """Carga las tablas de la base de datos seleccionada y las muestra en el Dropdown."""
    if not var.nombre_bd:
        messagebox.showwarning("Advertencia", "Primero selecciona una base de datos.")
        return
    try:
        with sqlite3.connect(var.nombre_bd) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = [row[0] for row in cursor.fetchall()]

            if tablas:
                tablas_combo["values"] = tablas  # Insertar las tablas en el dropdown
                tablas_combo.current(0)
            else:
                tablas_combo["values"] = []
                messagebox.showwarning("Advertencia", "No hay tablas en esta base de datos.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las tablas: {e}")

def cargar_columnas(tablas_combo, columnas_x_combo, columnas_y_combo):
    """Carga las columnas de la tabla seleccionada y las muestra en los Dropdowns de ejes X e Y."""
    if not var.nombre_bd:
        messagebox.showwarning("Advertencia", "Primero selecciona una base de datos.")
        return
    tabla_seleccionada = tablas_combo.get()
    if not tabla_seleccionada:
        messagebox.showwarning("Advertencia", "Selecciona una tabla primero.")
        return
    try:
        with sqlite3.connect(var.nombre_bd) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({tabla_seleccionada});")
            columnas = [row[1] for row in cursor.fetchall()]

            if columnas:
                columnas_x_combo["values"] = columnas  # Insertar las columnas en el dropdown de eje X
                columnas_y_combo["values"] = columnas  # Insertar las columnas en el dropdown de eje Y
                columnas_x_combo.current(0)
                columnas_y_combo.current(0)
            else:
                columnas_x_combo["values"] = []
                columnas_y_combo["values"] = []
                messagebox.showwarning("Advertencia", "No hay columnas en esta tabla.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las columnas: {e}")

def generar_grafico(tablas_combo, columnas_x_combo, columnas_y_combo, tipo_grafico_combo, frame_principal):
    """Genera un gráfico basado en la selección del usuario."""
    tabla = tablas_combo.get()
    x_col = columnas_x_combo.get()
    y_col = columnas_y_combo.get()
    tipo_grafico = tipo_grafico_combo.get()

    if not var.nombre_bd or not tabla or not x_col or not y_col:
        messagebox.showwarning("Advertencia", "Asegúrate de seleccionar la base de datos, tabla y columnas antes de generar el gráfico.")
        return

    datos = obtener_datos_bd(var.nombre_bd, tabla)
    if datos is None or datos.empty:
        messagebox.showwarning("Advertencia", "No hay datos para generar el gráfico.")
        return

    if not pd.api.types.is_numeric_dtype(datos[y_col]):
        messagebox.showerror("Error", f"La columna '{y_col}' debe contener datos numéricos para generar el gráfico.")
        return

    datos[x_col] = datos[x_col].astype(str)

    fig, ax = plt.subplots(figsize=(12, 8))
    try:
        if tipo_grafico == "Barras":
            datos.groupby(x_col)[y_col].sum().plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
        elif tipo_grafico == "Líneas":
            datos.groupby(x_col)[y_col].sum().plot(kind='line', ax=ax, marker='o', color='blue')
        elif tipo_grafico == "Pastel":
            datos.groupby(x_col)[y_col].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90)
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el gráfico: {e}")
        return

    ax.set_title(f"Gráfico de tipo {tipo_grafico}", fontsize=16, fontweight='bold')
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)

    if tipo_grafico != "Pastel":
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.margins(x=0.01)

    plt.tight_layout()

    grafico_frame = tk.Frame(frame_principal,  width=800, height=600)
    grafico_frame.pack(fill="both", expand=True)
    grafico_canvas = FigureCanvasTkAgg(fig, grafico_frame)
    grafico_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    global fig_actual
    fig_actual = fig
    
    
def abrir_wizard(frame_principal):
    # Crear la ventana del asistente
    wizard = frame_principal
    global fig_actual  # Se usa una variable global para almacenar la figura
    

    tabla_seleccionada = tk.StringVar()
    columna_x = tk.StringVar()
    columna_y = tk.StringVar()
    tipo_grafico = tk.StringVar(value="Barras")

    # Paso 1: Selección de tabla
    paso1 = ttk.Frame(wizard)
    paso1.pack(fill="both", expand=True)

    ttk.Label(paso1, text="Selecciona una tabla:", font=("Arial", 10)).pack(pady=5)
    tablas_combo = ttk.Combobox(paso1, textvariable=tabla_seleccionada, state="readonly")
    tablas_combo.pack(pady=10)


    ttk.Button(paso1, text="Seleccionar Base de Datos", command=seleccionar_bd).pack(pady=5)
    ttk.Button(paso1, text="Cargar Tablas", command=lambda: cargar_tablas(tablas_combo)).pack(pady=5)

    # Paso 2: Selección de columnas y gráfico
    paso2 = ttk.Frame(wizard)

    ttk.Label(paso2, text="Selecciona columna para eje X:", font=("Arial", 10)).pack()
    columnas_x_combo = ttk.Combobox(paso2, textvariable=columna_x, state="readonly")
    columnas_x_combo.pack()
    
    ttk.Label(paso2, text="Selecciona columna para eje Y:", font=("Arial", 10)).pack()
    columnas_y_combo = ttk.Combobox(paso2, textvariable=columna_y, state="readonly")
    columnas_y_combo.pack()
    
    ttk.Button(paso2, text="Cargar Columnas", command=lambda: cargar_columnas(tablas_combo, columnas_x_combo, columnas_y_combo)).pack()
    

    ttk.Label(paso2, text="Selecciona el tipo de gráfico:", font=("Arial", 10)).pack(pady=5)
    tipo_grafico_combo = ttk.Combobox(paso2, textvariable=tipo_grafico, state="readonly", values=["Barras", "Líneas", "Pastel"])
    tipo_grafico_combo.pack(pady=5)

    # Paso 3: Generación del gráfico
    paso3 = ttk.Frame(wizard)
    
    ttk.Button(paso3, text="Generar Gráfico", command=lambda: generar_grafico(tablas_combo, columnas_x_combo, columnas_y_combo, tipo_grafico_combo, frame_principal)).pack(pady=5)
    

    # Navegación entre pasos
    pasos = [paso1, paso2, paso3]
    paso_actual = 0

    def mostrar_paso(index):
        nonlocal paso_actual
        pasos[paso_actual].pack_forget()
        pasos[index].pack(fill="both", expand=True)
        paso_actual = index

    ttk.Button(wizard, text="Siguiente", command=lambda: mostrar_paso(paso_actual + 1)).pack(side="right", pady=10)
    ttk.Button(wizard, text="Anterior", command=lambda: mostrar_paso(paso_actual - 1)).pack(side="left", pady=10)

    mostrar_paso(0)


def exportar_pdf():
        """Exporta el gráfico actual a un archivo PDF."""
        global fig_actual
        if 'fig_actual' in globals() and fig_actual is not None:
            exportar_grafico_pdf(fig_actual)
        else:
            messagebox.showwarning("Advertencia", "No hay un gráfico disponible para exportar.")

# Aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplicación Principal")
    root.geometry("600x600")

    frame_derecho = tk.Frame(root)
    frame_derecho.pack(fill="both", expand=True)

    ttk.Button(root, text="Abrir Asistente", command=lambda: abrir_wizard(frame_derecho)).pack()

    root.mainloop()
