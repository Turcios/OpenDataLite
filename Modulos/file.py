import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
import sqlite3

# Función para abrir una nueva ventana después de cargar el archivo
def abrir_nueva_ventana(contenido,file_path):
    nueva_ventana = tk.Toplevel()  # Crear nueva ventana
    nueva_ventana.title("OpenDataLite")

    #Etiqueta de campo del nombre de la base de datos
    label_nombre_bd = tk.Label(nueva_ventana, text="Nombre base de datos:")
    label_nombre_bd.pack(pady=5)

    # Entrada de texto para el nombre
    entry_nombre_bd = tk.Entry(nueva_ventana)
    entry_nombre_bd.pack(pady=5)

    #Etiqueta de campo del nombre de la base de datos
    label_nombre_tabla = tk.Label(nueva_ventana, text="Nombre de la tabla")
    label_nombre_tabla.pack(pady=5)

    # Entrada de texto para el nombre
    entry_nombre_tabla = tk.Entry(nueva_ventana)
    entry_nombre_tabla.pack(pady=5)    
    

    # Etiqueta para mostrar el contenido del archivo
    label_contenido = tk.Label(nueva_ventana, text="Contenido del archivo:")
    label_contenido.pack(pady=10)

    # Botón de enviar
    boton_enviar = tk.Button(nueva_ventana, text="Enviar", command=lambda: mostrar_datos(entry_nombre_bd.get(),entry_nombre_tabla.get(),file_path,nueva_ventana))
    boton_enviar.pack(pady=10)

# Función para mostrar los datos ingresados en el formulario
def mostrar_datos(nombre_bd,nombre_tabla,file_path,nueva_ventana):
    if file_path:
        try:
            # Leer el CSV con pandas
            df = pd.read_csv(file_path)
            
            # Conectar a la base de datos SQLite (se crea si no existe)
            conexion = sqlite3.connect(nombre_bd+".db")
            
            # Insertar el DataFrame en una tabla de SQLite
            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
            
            # Cerrar la conexión
            conexion.close()
            
            # Mostrar un mensaje de éxito
            messagebox.showinfo("Éxito", "El archivo CSV ha sido cargado en la base de datos correctamente.")
        except Exception as e:
            # Mostrar un mensaje de error si algo falla
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    #cierra la ventana al enviar los datos
    nueva_ventana.destroy()
    
def nueva_archivo():
    file_path = filedialog.askopenfilename(
    title="Seleccionar archivo CSV",
    filetypes=[("CSV files", "*.csv")]  # Limita a solo archivos CSV
    )
    # Verificar si se seleccionó un archivo
    if file_path:
        # Abrir y leer el archivo CSV
        with open(file_path, 'r') as file:
            content = file.read()
            print("Contenido del archivo CSV:")
            print(content)
            abrir_nueva_ventana(content, file_path)  # Llamar a la función para abrir la nueva ventana
    else:
        print("No se seleccionó ningún archivo.")
    
    
