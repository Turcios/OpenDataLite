import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd

def abrir_wizard():
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("OpenDataLite")
    nueva_ventana.geometry("600x400")

    # Variables para el wizard
    tabla_seleccionada = tk.StringVar()
    eje_x = tk.StringVar()
    eje_y = tk.StringVar()
    tipo_grafico = tk.StringVar(value="Barras")

    # Paso 1: Selección de tabla
    paso1 = ttk.Frame(nueva_ventana)
    paso1.pack(fill="both", expand=True)

    ttk.Label(paso1, text="Selecciona una tabla:").pack(pady=10)
    tablas_combo = ttk.Combobox(paso1, textvariable=tabla_seleccionada)
    tablas_combo.pack()

    def cargar_columnas():
        tabla = tabla_seleccionada.get()
        if not tabla:
            return
        columnas = obtener_columnas(tabla)  # Función para obtener columnas de la tabla
        eje_x_combo["values"] = columnas
        eje_y_combo["values"] = columnas

    ttk.Button(paso1, text="Cargar Columnas", command=cargar_columnas).pack(pady=10)

    # Paso 2: Selección de ejes
    paso2 = ttk.Frame(nueva_ventana)
    ttk.Label(paso2, text="Selecciona el eje X:").pack(pady=10)
    eje_x_combo = ttk.Combobox(paso2, textvariable=eje_x)
    eje_x_combo.pack()

    ttk.Label(paso2, text="Selecciona el eje Y:").pack(pady=10)
    eje_y_combo = ttk.Combobox(paso2, textvariable=eje_y)
    eje_y_combo.pack()

    # Paso 3: Tipo de gráfico
    paso3 = ttk.Frame(nueva_ventana)
    ttk.Label(paso3, text="Selecciona el tipo de gráfico:").pack(pady=10)
    tipos = ["Barras", "Líneas", "Pastel"]
    tipo_grafico_combo = ttk.Combobox(paso3, textvariable=tipo_grafico, values=tipos)
    tipo_grafico_combo.pack()

    # Paso 4: Previsualización
    paso4 = ttk.Frame(nueva_ventana)
    canvas_frame = ttk.Frame(paso4)
    canvas_frame.pack(fill="both", expand=True)

    def generar_grafico():
        tabla = tabla_seleccionada.get()
        x = eje_x.get()
        y = eje_y.get()
        tipo = tipo_grafico.get()

        if tabla and x and y:
            datos = obtener_datos(tabla, x, y)  # Función para obtener datos de la BD
            fig, ax = plt.subplots()

            if tipo == "Barras":
                ax.bar(datos[x], datos[y])
            elif tipo == "Líneas":
                ax.plot(datos[x], datos[y])
            elif tipo == "Pastel":
                ax.pie(datos[y], labels=datos[x], autopct="%1.1f%%")

            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    ttk.Button(paso4, text="Generar Gráfico", command=generar_grafico).pack()

    # Navegación entre pasos
    pasos = [paso1, paso2, paso3, paso4]
    paso_actual = 0

    def mostrar_paso(index):
        nonlocal paso_actual
        pasos[paso_actual].pack_forget()
        pasos[index].pack(fill="both", expand=True)
        paso_actual = index

    ttk.Button(nueva_ventana, text="Siguiente", command=lambda: mostrar_paso(paso_actual + 1)).pack(side="right", pady=10)
    ttk.Button(nueva_ventana, text="Anterior", command=lambda: mostrar_paso(paso_actual - 1)).pack(side="left", pady=10)

    mostrar_paso(0)

def obtener_columnas(tabla):
    # Conectar a SQLite y devolver las columnas de la tabla seleccionada
    with sqlite3.connect("mi_base_de_datos.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({tabla})")
        return [col[1] for col in cursor.fetchall()]

def obtener_datos(tabla, x, y):
    # Conectar a SQLite y obtener datos de las columnas seleccionadas
    query = f"SELECT {x}, {y} FROM {tabla}"
    with sqlite3.connect("mi_base_de_datos.db") as conn:
        return pd.read_sql(query, conn)

