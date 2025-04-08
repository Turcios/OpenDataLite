import tkinter as tk
import sqlite3
import pandas as pd
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modulos.graficos import exportar_grafico_pdf
import os
import modulos.variable as var  # Para almacenar la base de datos seleccionada

# Contexto global para almacenar el nombre de la base de datos seleccionada
#db_context = {"nombre_bd": None}

class AsistenteGraficos:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.fig_actual = None

        self.tabla = tk.StringVar()
        self.columna_x = tk.StringVar()
        self.columna_y = tk.StringVar()
        self.tipo_grafico = tk.StringVar(value="Grafico")

        self._construir_ui()

    def _construir_ui(self):
        # Paso 1
        ttk.Button(self.frame, text="Cargar Tablas", command=self.cargar_tablas).pack(pady=5)

        ttk.Label(self.frame, text="Tabla:").pack()
        self.tablas_combo = ttk.Combobox(self.frame, textvariable=self.tabla, state="readonly")
        self.tablas_combo.pack(pady=5)

        # Paso 2
        ttk.Button(self.frame, text="Cargar Columnas", command=self.cargar_columnas).pack(pady=5)

        ttk.Label(self.frame, text="Columna X:").pack()
        self.columnas_x_combo = ttk.Combobox(self.frame, textvariable=self.columna_x, state="readonly")
        self.columnas_x_combo.pack(pady=5)

        ttk.Label(self.frame, text="Columna Y:").pack()
        self.columnas_y_combo = ttk.Combobox(self.frame, textvariable=self.columna_y, state="readonly")
        self.columnas_y_combo.pack(pady=5)

        #ttk.Label(self.frame, text="Tipo de gráfico:").pack()
        #self.tipo_grafico_combo = ttk.Combobox(self.frame, textvariable=self.tipo_grafico, state="readonly", values=[])
        #self.tipo_grafico_combo.pack(pady=5)
        #self.tipo_grafico_label = ttk.Label(self.frame,textvariable=self.tipo_grafico)
        #self.tipo_grafico_label.pack()

        # Paso 3
        ttk.Button(self.frame, text="Generar Gráfico", command=self.generar_grafico).pack(pady=10)

        # Contenedor de gráfico
        self.grafico_frame = tk.Frame(self.frame, width=800, height=600)
        self.grafico_frame.pack(fill="both", expand=True)

        # Exportar
        ttk.Button(self.frame, text="Exportar PDF", command=self.exportar_pdf).pack(pady=5)

    def seleccionar_bd(self):
        """Muestra una lista de bases de datos .db disponibles para seleccionar."""
        carpeta_bd = os.path.join(os.getcwd(), "bd")  # Carpeta donde tienes las bases de datos
        if not os.path.exists(carpeta_bd):
            os.makedirs(carpeta_bd)

        archivos_db = [f for f in os.listdir(carpeta_bd) if f.endswith(".db")]

        if not archivos_db:
            messagebox.showinfo("Sin bases de datos", "No se encontraron archivos .db en la carpeta 'bd'.")
            return

        ventana = tk.Toplevel(self.frame)
        ventana.title("Seleccionar Base de Datos")
        ventana.geometry("300x150")

        tk.Label(ventana, text="Selecciona una base de datos:").pack(pady=10)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, values=archivos_db, state="readonly")
        combo.pack(pady=5)
        combo.current(0)

        def confirmar():
            var.nombre_bd = os.path.join(carpeta_bd, seleccion.get())
            messagebox.showinfo("Base de Datos Seleccionada", f"Usando la base de datos:\n{seleccion.get()}")
            ventana.destroy()

        ttk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)

    def cargar_tablas(self):
        if not var.nombre_bd:
            messagebox.showwarning("Advertencia", "Primero selecciona una base de datos.")
            return
        try:
            with sqlite3.connect(var.nombre_bd) as conn:
                tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
                self.tablas_combo["values"] = tablas["name"].tolist()
                if tablas.shape[0] > 0:
                    self.tablas_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las tablas: {e}")

    def cargar_columnas(self):
        if not var.nombre_bd or not self.tabla.get():
            messagebox.showwarning("Advertencia", "Selecciona una base de datos y tabla.")
            return
        try:
            with sqlite3.connect(var.nombre_bd) as conn:
                query = f"PRAGMA table_info('{self.tabla.get()}')"
                columnas = pd.read_sql(query, conn)
                col_names = columnas["name"].tolist()
                self.columnas_x_combo["values"] = col_names
                self.columnas_y_combo["values"] = col_names
                if col_names:
                    self.columnas_x_combo.current(0)
                    self.columnas_y_combo.current(1 if len(col_names) > 1 else 0)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las columnas: {e}")

    def generar_grafico(self):
        tabla = self.tabla.get()
        x_col = self.columna_x.get()
        y_col = self.columna_y.get()
        tipo = self.tipo_grafico.get()

        if not all([var.nombre_bd, tabla, x_col, y_col]):
            messagebox.showwarning("Advertencia", "Selecciona tabla y columnas.")
            return

        try:
            df = pd.read_sql(f"SELECT * FROM '{tabla}'", sqlite3.connect(var.nombre_bd))
        except Exception as e:
            messagebox.showerror("Error", f"Error leyendo la tabla: {e}")
            return

        if df.empty or x_col not in df or y_col not in df:
            messagebox.showwarning("Advertencia", "Datos insuficientes para graficar.")
            return

        # Elegir tipo óptimo si está en automático
        if tipo == "Grafico":
            tipo = self._seleccionar_tipo_optimo(df, x_col, y_col)

        # Verificar que y_col sea numérico
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            messagebox.showerror("Error", f"La columna '{y_col}' no es numérica.")
            return

        # Convertir X a string para agrupación
        df[x_col] = df[x_col].astype(str)

        # Limpiar gráfico previo
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 6))

        try:
            agrupado = df.groupby(x_col)[y_col].sum()
            if tipo == "Barras":
                agrupado.plot(kind="bar", ax=ax)
            elif tipo == "Líneas":
                agrupado.plot(kind="line", ax=ax, marker='o')
            elif tipo == "Pastel":
                agrupado.plot(kind="pie", ax=ax, autopct='%1.1f%%')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo graficar: {e}")
            return

        ax.set_title(f"{tipo} de {y_col} por {x_col}")
        if tipo != "Pastel":
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig_actual = fig

    def _seleccionar_tipo_optimo(self, df, x_col, y_col):
        """Decide el gráfico más adecuado según los datos"""
        x_unique = df[x_col].nunique()
        if x_unique < 6:
            return "Pastel"
        elif pd.api.types.is_datetime64_any_dtype(df[x_col]) or "fecha" in x_col.lower():
            return "Líneas"
        else:
            return "Barras"

    def exportar_pdf(self):
        """Exporta el gráfico actual a un archivo PDF."""
        if self.fig_actual:
            exportar_grafico_pdf(self.fig_actual)
        else:
            messagebox.showwarning("Advertencia", "No hay un gráfico disponible para exportar.")


# Aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Asistente de Gráficos")
    root.geometry("800x700")

    app = AsistenteGraficos(root)

    root.mainloop()