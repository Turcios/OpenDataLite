import tkinter as tk
from tkinter import ttk 
import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modulos.graficos import exportar_grafico_pdf

# Contexto global para almacenar el nombre de la base de datos seleccionada
db_context = {"nombre_bd": None}

def seleccionar_bd():
    ruta_bd = filedialog.askopenfilename(
        title="Seleccionar base de datos",
        filetypes=[("Archivos SQLite", "*.db")]
    )
    if ruta_bd:
        db_context["nombre_bd"] = ruta_bd
        messagebox.showinfo("Éxito", f"Base de datos seleccionada: {ruta_bd}")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna base de datos.")

def obtener_datos_bd(nombre_bd, tabla):
    try:
        with sqlite3.connect(nombre_bd) as conn:
            return pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos: {e}")
        return None

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

    def cargar_tablas():
        nombre_bd = db_context.get("nombre_bd")
        if not nombre_bd:
            messagebox.showwarning("Advertencia", "Primero selecciona una base de datos.")
            return
        try:
            with sqlite3.connect(nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tablas = [row[0] for row in cursor.fetchall()]
                tablas_combo["values"] = tablas
                if tablas:
                    tablas_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las tablas: {e}")

    ttk.Button(paso1, text="Seleccionar Base de Datos", command=seleccionar_bd).pack(pady=5)
    ttk.Button(paso1, text="Cargar Tablas", command=cargar_tablas).pack(pady=5)

    # Paso 2: Selección de columnas y gráfico
    paso2 = ttk.Frame(wizard)

    ttk.Label(paso2, text="Selecciona la columna para el eje X:", font=("Arial", 10)).pack()
    columnas_x_combo = ttk.Combobox(paso2, textvariable=columna_x, state="readonly")
    columnas_x_combo.pack(pady=5)

    ttk.Label(paso2, text="Selecciona la columna para el eje Y:", font=("Arial", 10)).pack()
    columnas_y_combo = ttk.Combobox(paso2, textvariable=columna_y, state="readonly")
    columnas_y_combo.pack()

    ttk.Label(paso2, text="Selecciona el tipo de gráfico:", font=("Arial", 10)).pack()
    ttk.Combobox(paso2, textvariable=tipo_grafico, state="readonly", values=["Barras", "Líneas", "Pastel"]).pack()

    def cargar_columnas():
        tabla = tabla_seleccionada.get()
        nombre_bd = db_context.get("nombre_bd")
        if not tabla or not nombre_bd:
            messagebox.showwarning("Advertencia", "Primero selecciona una tabla.")
            return
        datos = obtener_datos_bd(nombre_bd, tabla)
        if datos is not None:
            columnas = datos.columns.tolist()
            columnas_x_combo["values"] = columnas
            columnas_y_combo["values"] = columnas
            if columnas:
                columnas_x_combo.current(0)
                columnas_y_combo.current(0)

    ttk.Button(paso2, text="Cargar Columnas", command=cargar_columnas).pack(pady=10)

    # Paso 3: Generación del gráfico
    paso3 = ttk.Frame(wizard)

    def generar_grafico():
        tabla = tabla_seleccionada.get()
        x_col = columna_x.get()
        y_col = columna_y.get()
        grafico = tipo_grafico.get()

        if not tabla or not x_col or not y_col:
            messagebox.showwarning("Advertencia", "Selecciona la tabla y las columnas antes de generar el gráfico.")
            return

        nombre_bd = db_context.get("nombre_bd")
        datos = obtener_datos_bd(nombre_bd, tabla)

        if datos is None or datos.empty:
            messagebox.showwarning("Advertencia", "No hay datos para generar el gráfico.")
            return

        if not pd.api.types.is_numeric_dtype(datos[y_col]):
            messagebox.showerror("Error", f"La columna '{y_col}' debe contener datos numéricos para generar el gráfico.")
            return

        datos[x_col] = datos[x_col].astype(str)

        fig, ax = plt.subplots(figsize=(10, 6))  # Aumentar el tamaño del gráfico para más claridad
        try:
            if grafico == "Barras":
                datos.groupby(x_col)[y_col].sum().plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
            elif grafico == "Líneas":
                datos.groupby(x_col)[y_col].sum().plot(kind='line', ax=ax, marker='o', color='blue')
            elif grafico == "Pastel":
                datos.groupby(x_col)[y_col].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el gráfico: {e}")
            return

        ax.set_title(f"Gráfico de tipo {grafico}", fontsize=16, fontweight='bold')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)

        if grafico != "Pastel":
            ax.tick_params(axis='x', rotation=45, labelsize=10)
            ax.tick_params(axis='y', labelsize=10)
            ax.margins(x=0.01)

        plt.tight_layout()

        grafico_frame = tk.Frame(frame_principal)
        grafico_frame.pack(fill="both", expand=True)
        grafico_canvas = FigureCanvasTkAgg(fig, grafico_frame)
        grafico_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        global fig_actual
        fig_actual = fig  # Guardar la figura generada

    ttk.Button(paso3, text="Generar Gráfico", command=generar_grafico).pack(pady=10)
    

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

    ttk.Button(root, text="Abrir Asistente", command=lambda: abrir_wizard(frame_derecho)).pack(pady=20)

    root.mainloop()