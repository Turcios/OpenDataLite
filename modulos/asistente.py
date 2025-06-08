import tkinter as tk
import sqlite3
import pandas as pd
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image, ImageTk
import os
import modulos.variable as var
import numpy as np
from io import BytesIO
from datetime import datetime
from modulos.idioma import obtener_texto
from modulos.utils import obtener_ruta_recurso


# Contexto global para almacenar el nombre de la base de datos seleccionada
db_context = {"nombre_bd": None}

fig_actual = None
df_actual = None


def buscar_bases_datos():
    #Busca archivos .db en el directorio actual y devuelve una lista de nombres.
    carpeta_busqueda = os.getcwd()  # Puedes cambiarlo si deseas otra ruta específica
    return [f for f in os.listdir(carpeta_busqueda) if f.endswith(".db")]


def obtener_datos_bd(nombre_bd, tabla):
    try:
        with sqlite3.connect(nombre_bd) as conn:
            return pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
    except Exception as e:
        messagebox.showerror(obtener_texto("error"), f"{obtener_texto('warning_no_db_selected')}: {e}")
        return None

def cargar_tablas(tablas_combo):
    #Carga las tablas de la base de datos seleccionada y las muestra en el Dropdown.
    if not var.nombre_bd:
        messagebox.showwarning(obtener_texto("warning"),obtener_texto('do_not_select_db'))
        return
    try:
        with sqlite3.connect(var.nombre_bd) as conn:
            tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
            tablas_combo["values"] = tablas["name"].tolist()
            if not tablas.empty:
                tablas_combo.current(0)
    except Exception as e:
        messagebox.showerror(obtener_texto("error"), f"{obtener_texto('error_load_table')} {e}")

def cargar_columnas(tablas_combo, columnas_x_combo, columnas_y_combo,vista):
    #Carga las columnas de la tabla seleccionada y las muestra en los Dropdowns de ejes X e Y.
    if not var.nombre_bd or not tablas_combo.get():
        messagebox.showwarning(obtener_texto("warning"), obtener_texto("select_database_table"))
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

            df_preview = pd.read_sql(f"SELECT * FROM '{tablas_combo.get()}' LIMIT 10", conn)
            vista.config(state='normal')
            vista.delete("1.0", tk.END)
            vista.insert(tk.END, df_preview.to_string(index=False))
            vista.config(state='disabled')
    except Exception as e:
        messagebox.showerror(obtener_texto("error"), f"{obtener_texto('no_column_select')} {e}")

def generar_grafico(tablas_combo, columnas_x_combo, columnas_y_combo, tipo_grafico, frame_grafico, volver_btn):
    #Genera un gráfico basado en la selección del usuario.
    global fig_actual
    global df_actual
    

    if not all([var.nombre_bd, tablas_combo.get(), columnas_y_combo.get()]):
        messagebox.showwarning(obtener_texto("warning"), obtener_texto('select_table_columns'))
        return

    try:
        df = pd.read_sql(f"SELECT * FROM '{tablas_combo.get()}'", sqlite3.connect(var.nombre_bd))
        df_actual = df.copy()
    except Exception as e:
        messagebox.showerror(obtener_texto("error"), f"{obtener_texto('error_reading_table')}: {e}")
        return

    if df.empty or columnas_y_combo.get() not in df:
        messagebox.showwarning(obtener_texto("warning"),obtener_texto('Insufficient_data_graph'))
        return

    if tipo_grafico.get() == "Histograma":
        if not pd.api.types.is_numeric_dtype(df[columnas_y_combo.get()]):
            messagebox.showerror(obtener_texto("error"), f"La columna '{columnas_y_combo.get()}' no es numérica.")
            return
    else:
        if columnas_x_combo.get() not in df:
            messagebox.showwarning(obtener_texto("warning"),obtener_texto('Insufficient_data_graph'))
            return
        df[columnas_x_combo.get()] = df[columnas_x_combo.get()].astype(str)

    # Limpiar gráficos anteriores
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Crear nuevo gráfico
    fig, ax = plt.subplots(figsize=(8, 3.5))
    
    try:
        if tipo_grafico.get() == "Barras":
            agrupado = df.groupby(columnas_x_combo.get())[columnas_y_combo.get()].sum()
            agrupado.plot(kind="bar", ax=ax)
        elif tipo_grafico.get() == "Líneas":
            agrupado = df.groupby(columnas_x_combo.get())[columnas_y_combo.get()].sum()
            agrupado.plot(kind="line", ax=ax, marker='o')
        elif tipo_grafico.get() == "Pastel":
            agrupado = df.groupby(columnas_x_combo.get())[columnas_y_combo.get()].sum()
            agrupado.plot(kind="pie", ax=ax, autopct='%1.1f%%')
        elif tipo_grafico.get() == "Histograma":
            df[columnas_y_combo.get()].plot(kind="hist", bins=10, ax=ax, edgecolor='black')
    except Exception as e:
        messagebox.showerror(obtener_texto("error"), f"{obtener_texto('error_generate_chart')} {e}")
        return

    ax.set_title(f"{tipo_grafico.get()} de {columnas_y_combo.get()}")
    if tipo_grafico.get() !=  ["Pastel", "Histograma"]:
        ax.set_xlabel(columnas_x_combo.get())
        ax.set_ylabel(columnas_y_combo.get())
        ax.tick_params(axis='x', rotation=45)
    elif tipo_grafico.get() == "Histograma":
        ax.set_xlabel(columnas_y_combo.get())
        ax.set_ylabel("Frecuencia")

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
    
 
def cargar_imagen(nombre_archivo):
    try:
        ruta_imagen = obtener_ruta_recurso(nombre_archivo)
        print(f"Cargando imagen: {ruta_imagen}")
        imagen = Image.open(ruta_imagen).resize((48, 48), Image.LANCZOS)
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"Error cargando {nombre_archivo}: {e}")
        return None
    


def abrir_wizard(frame_graficos):
    # Variables
    tabla = tk.StringVar()
    columna_x = tk.StringVar()
    columna_y = tk.StringVar()
    # Al inicio de abrir_wizard, justo después de crear tipo_grafico
    tipo_grafico = tk.StringVar(value="Barras")

    # Cargar imágenes
    img_barras = cargar_imagen("barras.png")
    print("Imagen barras cargada")
    img_lineas = cargar_imagen("lineas.png")
    print("Líneas OK")
    img_pastel = cargar_imagen("pastel.png")
    print("Pastel OK")
    img_histograma = cargar_imagen("histogram.png")
    print("histograma OK")

    # Contenedor principal
    contenedor = ttk.Frame(frame_graficos, padding=10)
    contenedor.pack(fill="both", expand=True)

    contenedor.columnconfigure(0, weight=1)
    contenedor.columnconfigure(1, weight=2)
    contenedor.rowconfigure(0, weight=1)
    contenedor.rowconfigure(1, weight=1)
    
    # -------- FORMULARIO CON SCROLLBAR ----------
    formulario_frame = ttk.LabelFrame(contenedor, text=obtener_texto("configuration"), padding=0)
    formulario_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=(0,10))

    formulario_canvas = tk.Canvas(formulario_frame, borderwidth=0, highlightthickness=0)
    formulario_scrollbar = ttk.Scrollbar(formulario_frame, orient="vertical", command=formulario_canvas.yview)
    formulario_scrollbar.pack(side="right", fill="y")
    formulario_canvas.pack(side="left", fill="both", expand=True)

    formulario_interior = ttk.Frame(formulario_canvas, padding=10)
    formulario_canvas.create_window((0, 0), window=formulario_interior, anchor="nw")

    # Ajustar el ancho del interior al ancho del canvas
    def ajustar_ancho(event):
        formulario_canvas.itemconfig("all", width=event.width)
    formulario_canvas.bind("<Configure>", ajustar_ancho)

    formulario_interior.bind(
        "<Configure>",
        lambda e: formulario_canvas.configure(scrollregion=formulario_canvas.bbox("all"))
    )
    
    formulario_canvas.configure(yscrollcommand=formulario_scrollbar.set)
    formulario_canvas.bind_all("<MouseWheel>", lambda e: formulario_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # ------- WIDGETS del formulario -------
    formulario_interior.columnconfigure(0, weight=1)

    ttk.Button(formulario_interior, text=obtener_texto("load_tables"), command=lambda: cargar_tablas(tablas_combo)).grid(row=0, column=0, sticky="ew", pady=5)

    ttk.Label(formulario_interior, text=obtener_texto("table")).grid(row=1, column=0, sticky="w", pady=(10,2))
    tablas_combo = ttk.Combobox(formulario_interior, textvariable=tabla, state="readonly")
    tablas_combo.grid(row=2, column=0, sticky="ew", pady=2)

    ttk.Button(formulario_interior, text=obtener_texto("load_column"), command=lambda: cargar_columnas(tabla, columnas_x_combo, columnas_y_combo, vista)).grid(row=3, column=0, sticky="ew", pady=10)

    ttk.Label(formulario_interior, text=obtener_texto("column_x")).grid(row=4, column=0, sticky="w", pady=(10,2))
    columnas_x_combo = ttk.Combobox(formulario_interior, textvariable=columna_x, state="readonly")
    columnas_x_combo.grid(row=5, column=0, sticky="ew", pady=2)

    ttk.Label(formulario_interior, text=obtener_texto("column_y")).grid(row=6, column=0, sticky="w", pady=(10,2))
    columnas_y_combo = ttk.Combobox(formulario_interior, textvariable=columna_y, state="readonly")
    columnas_y_combo.grid(row=7, column=0, sticky="ew", pady=2)

    ttk.Label(formulario_interior, text=obtener_texto("chart_type")).grid(row=8, column=0, sticky="w", pady=(10,2))

    tipo_grafico_frame = ttk.Frame(formulario_interior)
    tipo_grafico_frame.grid(row=9, column=0, pady=5, sticky="ew")

    # Crear botones de imagen
    for img, tipo in zip(
        [img_barras, img_lineas, img_pastel, img_histograma],
        ["Barras", "Líneas", "Pastel", "Histograma"]
    ):
        if img:
            btn = tk.Button(tipo_grafico_frame, image=img, command=lambda t=tipo: tipo_grafico.set(t))
            btn.image = img
            btn.pack(side="left", padx=5)
        else:
            print(f"Imagen tipo {tipo} no carga. Se omite botón.")

    volver_btn = ttk.Button(formulario_interior, text="← Volver", command=lambda: volver(frame_graficos))
    volver_btn.grid(row=10, column=0, pady=15)
    volver_btn.grid_remove()

    # ------- VISTA PREVIA + BOTON ----------
    vista_y_boton_frame = ttk.Frame(contenedor)
    vista_y_boton_frame.grid(row=0, column=1, sticky="nsew", pady=(0,10))

    vista_y_boton_frame.columnconfigure(0, weight=1)
    vista_y_boton_frame.rowconfigure(0, weight=1)

    vista_frame = ttk.LabelFrame(vista_y_boton_frame, text=obtener_texto("query_preview"), padding=10)
    vista_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=5)

    vista_scroll = ttk.Scrollbar(vista_frame)
    vista_scroll.pack(side="right", fill="y")

    vista = tk.Text(vista_frame, height=10, wrap="none", background="#f5f5f5", relief="flat", yscrollcommand=vista_scroll.set)
    vista.pack(fill="both", expand=True)
    vista.config(state="disabled")
    vista_scroll.config(command=vista.yview)

    generar_btn = ttk.Button(vista_y_boton_frame, text=obtener_texto("generate_chart"), command=lambda: generar_grafico(tabla, columna_x, columna_y, tipo_grafico, grafico_frame, volver_btn))
    generar_btn.grid(row=1, column=0, sticky="ew", pady=(10,0))

    # ------- GRAFICO ABAJO ----------
    grafico_frame = ttk.LabelFrame(contenedor, text=obtener_texto("chart"), padding=(10, 10))
    grafico_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
    grafico_frame.configure(height=300)
    grafico_frame.pack_propagate(False)


def crear_pagina_con_encabezado(pdf, contenido_func, *contenido_args):
    #Crea una página con encabezado y contenido personalizado
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    # Logo pequeño en la esquina superior izquierda
    try:
        logo_img = obtener_ruta_recurso("logo1.jpg")
        logo_img = Image.open(logo_img).resize((40, 40), Image.Resampling.LANCZOS)
        logo_array = np.array(logo_img)

        # Insertar imagen como parte del eje (usando add_axes evita distorsión)
        fig.add_axes([0.05, 0.91, 0.08, 0.08]).imshow(logo_array)
        fig.axes[-1].axis('off')  # Oculta el marco del logo
    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")

    # Título centrado arriba
    fig.text(0.5, 0.95, "OpenDataLite", fontsize=14, ha='center')

    # Fecha a la derecha
    fecha = datetime.now()
    fecha_actual = f"{fecha.day}-{fecha.month}-{fecha.year}"
    fig.text(0.95, 0.95, fecha_actual, fontsize=10, ha='right')

    # Insertar el contenido (gráfico o tabla)
    contenido_func(fig, *contenido_args)

    # Guardar la página
    pdf.savefig(fig)
    plt.close(fig)


def insertar_grafico(fig, fig_actual):
    buf = BytesIO()
    fig_actual.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    img = Image.open(buf)
    arr = np.array(img)
    ax = fig.add_axes([0.05, 0.1, 0.9, 0.8])
    ax.imshow(arr)
    ax.axis('off')
    buf.close()


def insertar_tabla(fig, df_page):
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.75])
    ax.axis('off')
    tabla = ax.table(
        cellText=df_page.values,
        colLabels=df_page.columns,
        loc='center',
        cellLoc='center'
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)


def exportar_pdf():
    global fig_actual, df_actual

    if fig_actual is None or df_actual is None:
        messagebox.showwarning(obtener_texto("warning"), obtener_texto("generate_graph_first"))
        return

    # Elegir dónde guardar el PDF
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title=obtener_texto("save_report")
    )
    if not file_path:
        return

    with PdfPages(file_path) as pdf:
        # Página del gráfico
        crear_pagina_con_encabezado(pdf, insertar_grafico, fig_actual)

        # Páginas de tabla
        rows_per_page = 25
        num_pages = int(np.ceil(len(df_actual) / rows_per_page))

        for page in range(num_pages):
            start = page * rows_per_page
            end = start + rows_per_page
            df_page = df_actual.iloc[start:end]
            crear_pagina_con_encabezado(pdf, insertar_tabla, df_page)

    messagebox.showinfo(obtener_texto("success"), f"{obtener_texto('success_pdf')}:\n{file_path}")


           

# Aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title(obtener_texto("visualizing_charts"))
    root.geometry("900x600")

    abrir_wizard(root)
    
    root.mainloop()