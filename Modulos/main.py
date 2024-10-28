import tkinter as tk
from tkinter import messagebox, Text, Frame, END
from tkinter import ttk  # Importamos ttk para el Treeview
import file  # Archivo file.py que contiene funciones relacionadas con la carga de archivos y BD
import database  # Archivo database.py que contiene la función ejecutar_consulta
import sqlite3

def salir_app():
    root.quit()

def acerca_de():
    messagebox.showinfo("Acerca de", "V1 OpenDataLite")

# Crear la ventana principal

def ejecutar_sql():
    # Obtiene la consulta SQL del campo de texto
    sentencia_sql = caja_texto.get("1.0", END).strip()
    if not sentencia_sql:
        messagebox.showwarning("Entrada vacía", "Por favor ingresa una sentencia SQL.")
        return

    # Obtener el contexto actual de base de datos y tabla
    contexto = file.obtener_contexto()
    nombre_bd = contexto["nombre_bd"]
    nombre_tabla = contexto["nombre_tabla"]

    if not nombre_bd or not nombre_tabla:
        messagebox.showerror("Error", "No hay una base de datos o tabla cargada actualmente.")
        return

    # Reemplazar el nombre de tabla en la consulta
    sentencia_sql = sentencia_sql.replace("{tabla}", nombre_tabla)

    try:
        # Conexión a la base de datos y ejecución de la consulta
        with sqlite3.connect(nombre_bd) as conexion:
            cursor = conexion.cursor()
            cursor.execute(sentencia_sql)
            columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
            filas = cursor.fetchall()  # Obtener todas las filas de la consulta
            
            # Limpiar el Treeview antes de poblarlo con nuevos datos
            for item in treeview.get_children():
                treeview.delete(item)

            # Configurar las columnas del Treeview
            treeview["columns"] = ["Indice"] + columnas  # Añadir columna para el índice
            treeview["show"] = "headings"  # Mostrar encabezados de columnas
            
            # Configurar encabezados de columna en el Treeview
            treeview.heading("Indice", text="Indice")  # Encabezado para el índice
            treeview.column("Indice", width=40, anchor='center') # Ajuste de ancho para la columna del indice
            for col in columnas:
                treeview.heading(col, text=col)
                treeview.column(col, width=150, anchor='center')  # Ajuste de ancho para cada columna

            # Insertar filas en el Treeview con índice
            for idx, fila in enumerate(filas, start=1):
                treeview.insert("", "end", values=(idx,) + fila)  # Insertar índice + fila

            # Muestra un mensaje de éxito
            messagebox.showinfo("Resultado", "Consulta ejecutada exitosamente.")

    except sqlite3.OperationalError as e:
        # Mostrar mensaje de error en caso de que la consulta SQL falle
        messagebox.showerror("Error", f"Error en la consulta SQL:\n{e}")

def limpiar_consulta():
    # Borra el contenido de la caja de texto de consultas
    caja_texto.delete('1.0', END)

# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("OpenDataLite")
root.geometry("850x600")  # Aumentamos la altura para acomodar el Treeview

# Crear un contenedor principal
contenedor = tk.Frame(root)
contenedor.pack(fill="both", expand=True)

# Frames izquierdo y derecho
frame_izquierdo = tk.Frame(contenedor, width=200)
frame_izquierdo.pack(side="left", fill="both", expand=True)

frame_derecho = tk.Frame(contenedor, width=400)  # Ajusta el ancho como desees
frame_derecho.pack(side="right", fill="both", expand=True)

# Crear una etiqueta temporal en el frame izquierdo (será reemplazada con la estructura)
label_izquierda = tk.Label(frame_izquierdo, text="Estructura")
label_izquierda.pack(pady=10)

# Crear una etiqueta temporal en el frame derecho para otros datos
label_derecha = tk.Label(frame_derecho, text="Consultas")
label_derecha.pack(pady=10)

# Caja de texto para la consulta SQL
caja_texto = Text(frame_derecho, wrap='word', height=10)
caja_texto.pack(expand=True, fill='both', padx=10, pady=10)

# Frame para los botones
frame_botones = Frame(frame_derecho)
frame_botones.pack(pady=10)

# Botón para ejecutar la consulta SQL
boton_ejecutar = tk.Button(frame_botones, text="Ejecutar SQL", command=ejecutar_sql)
boton_ejecutar.grid(row=0, column=0, padx=5)

# Botón para limpiar la consulta
boton_limpiar = tk.Button(frame_botones, text="Limpiar", command=limpiar_consulta)
boton_limpiar.grid(row=0, column=1, padx=5)

# Frame para el Treeview y la scrollbar
frame_treeview = Frame(frame_derecho)
frame_treeview.pack(expand=True, fill='both', padx=10, pady=10)

# Crear Treeview para mostrar los resultados de la consulta SQL
treeview = ttk.Treeview(frame_treeview)
treeview.pack(side="left", expand=True, fill='both')

# Agregar una barra de desplazamiento vertical
scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Barra de menú
barra_menu = tk.Menu(root)


menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Importar", command=lambda: file.nueva_archivo(frame_izquierdo))
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir_app)

# Añadir el menú "Archivo" a la barra de menú
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

# Crear un menú "Ayuda"
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)

# Añadir el menú "Ayuda" a la barra de menú
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

# Configurar la ventana para que use la barra de menú
root.config(menu=barra_menu)

# Iniciar el bucle principal de la aplicación
root.mainloop()
