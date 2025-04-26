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

#def seleccionar_bd():
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

#def conectar_bd():
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
        messagebox.showwarning("Advertencia", "Primero cargue una base de datos.")
        return
    try:
        with sqlite3.connect(var.nombre_bd) as conn:
            tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
            tablas_combo["values"] = tablas["name"].tolist()
            if not tablas.empty:
                tablas_combo.current(0)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las tablas: {e}")

def cargar_columnas(tablas_combo, columnas_x_combo, columnas_y_combo,vista):
    """Carga las columnas de la tabla seleccionada y las muestra en los Dropdowns de ejes X e Y."""
    if not var.nombre_bd or not tablas_combo.get():
        messagebox.showwarning("Advertencia", "Selecciona una base de datos y una tabla.")
        return
    try:
        with sqlite3.connect(var.nombre_bd) as conn:
            columnas = pd.read_sql(f"PRAGMA table_info('{tablas_combo.get()}')", conn)
            col_names = columnas["name"].tolist()
            columnas_x_combo["values"] = col_names
            columnas_y_combo["values"] = col_names
            if col_names:
                columnas_x_combo.current(0)
                columnas_y_combo.current(1 if len(col_names) > 1 else 0)

            df_preview = pd.read_sql(f"SELECT * FROM '{tablas_combo.get()}' LIMIT 7", conn)
            vista.config(state='normal')
            vista.delete("1.0", tk.END)
            vista.insert(tk.END, df_preview.to_string(index=False))
            vista.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las columnas: {e}")

def generar_grafico(tablas_combo, columnas_x_combo, columnas_y_combo, tipo_grafico, frame_grafico, volver_btn):
    """Genera un gráfico basado en la selección del usuario."""
    global fig_actual
    if not all([var.nombre_bd, tablas_combo.get(), columnas_x_combo.get(), columnas_y_combo.get()]):
        messagebox.showwarning("Advertencia", "Selecciona tabla y columnas.")
        return

    try:
        df = pd.read_sql(f"SELECT * FROM '{tablas_combo.get()}'", sqlite3.connect(var.nombre_bd))
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo la tabla: {e}")
        return

    if df.empty or columnas_x_combo.get() not in df or columnas_y_combo.get() not in df:
        messagebox.showwarning("Advertencia", "Datos insuficientes para graficar.")
        return

    if not pd.api.types.is_numeric_dtype(df[columnas_y_combo.get()]):
        messagebox.showerror("Error", f"La columna '{columnas_y_combo.get()}' no es numérica.")
        return

    df[columnas_x_combo.get()] = df[columnas_x_combo.get()].astype(str)

    # Limpiar gráficos anteriores
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Crear nuevo gráfico
    fig, ax = plt.subplots(figsize=(8, 3.5))
    agrupado = df.groupby(columnas_x_combo.get())[columnas_y_combo.get()].sum()
    
    try:
        if tipo_grafico.get() == "Barras":
            agrupado.plot(kind="bar", ax=ax)
        elif tipo_grafico.get() == "Líneas":
            agrupado.plot(kind="line", ax=ax, marker='o')
        elif tipo_grafico.get() == "Pastel":
            agrupado.plot(kind="pie", ax=ax, autopct='%1.1f%%')
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el gráfico: {e}")
        return

    ax.set_title(f"{tipo_grafico.get()} de {columnas_y_combo.get()} por {columnas_x_combo.get()}")
    if tipo_grafico.get() != "Pastel":
        ax.set_xlabel(columnas_x_combo.get())
        ax.set_ylabel(columnas_y_combo.get())
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.X, pady=10)
    canvas.get_tk_widget().config(height=300)

    fig_actual = fig
    volver_btn.grid()
    volver_btn.tkraise()
    
def volver(root):
    for widget in root.winfo_children():
        widget.destroy()
    abrir_wizard(root)
    
def abrir_wizard(frame_graficos):
    # Crear la ventana del asistente
    tabla = tk.StringVar()
    columna_x = tk.StringVar()
    columna_y = tk.StringVar()
    tipo_grafico = tk.StringVar(value="Barras")

    contenedor = ttk.Frame(frame_graficos)
    contenedor.pack(fill="both", expand=True)

    contenedor.columnconfigure(0, weight=1)
    contenedor.columnconfigure(1, weight=2)

    formulario_frame = ttk.Frame(contenedor)
    formulario_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    #ttk.Button(formulario_frame, text="Seleccionar Base de Datos", command=seleccionar_bd).grid(row=0, column=0, sticky="w", pady=2)
    ttk.Button(formulario_frame, text="Cargar Tablas", command=lambda: cargar_tablas(tablas_combo)).grid(row=0, column=0, sticky="w", pady=2)
    ttk.Label(formulario_frame, text="Tabla:").grid(row=1, column=0, sticky="w")
    tablas_combo = ttk.Combobox(formulario_frame, textvariable=tabla, state="readonly")
    tablas_combo.grid(row=2, column=0, sticky="ew", pady=2)
    
    ttk.Button(formulario_frame, text="Cargar Columnas", command=lambda: cargar_columnas(tabla, columnas_x_combo, columnas_y_combo, vista)).grid(row=3, column=0, sticky="w", pady=2)
    ttk.Label(formulario_frame, text="Columna X:").grid(row=4, column=0, sticky="w")
    columnas_x_combo = ttk.Combobox(formulario_frame, textvariable=columna_x, state="readonly")
    columnas_x_combo.grid(row=5, column=0, sticky="ew", pady=2)

    ttk.Label(formulario_frame, text="Columna Y:").grid(row=6, column=0, sticky="w")
    columnas_y_combo = ttk.Combobox(formulario_frame, textvariable=columna_y, state="readonly")
    columnas_y_combo.grid(row=7, column=0, sticky="ew", pady=2)

    ttk.Label(formulario_frame, text="Tipo de gráfico:").grid(row=8, column=0, sticky="w")
    tipo_grafico_combo = ttk.Combobox(formulario_frame, textvariable=tipo_grafico, values=["Barras", "Líneas", "Pastel"], state="readonly")
    tipo_grafico_combo.grid(row=9, column=0, sticky="ew", pady=2)

    volver_btn = ttk.Button(formulario_frame, text="← Volver", command=lambda: volver(frame_graficos))
    volver_btn.grid(row=10, column=0, pady=5)
    volver_btn.grid_remove()

    ttk.Button(formulario_frame, text="Generar Gráfico", command=lambda: generar_grafico(tabla, columna_x, columna_y, tipo_grafico, grafico_frame, volver_btn)).grid(row=11, column=0, pady=10)

    vista_frame = ttk.Frame(contenedor)
    vista_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    vista = tk.Text(vista_frame, height=10, wrap="none")
    vista.pack(fill="both", expand=True)
    vista.config(state="disabled", bg="#f5f5f5")

    grafico_frame = tk.Frame(contenedor, bg="white", height=300)
    grafico_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    grafico_frame.pack_propagate(False)


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
    root.title("Visualización de Gráficos")
    root.geometry("900x600")

    abrir_wizard(root)

    root.mainloop()
