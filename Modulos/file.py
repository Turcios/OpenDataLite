import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk


# Función para abrir una nueva ventana después de cargar el archivo
def abrir_nueva_ventana(contenido):
    nueva_ventana = tk.Toplevel()  # Crear nueva ventana
    nueva_ventana.title("Contenido del Archivo CSV")

    # Etiqueta para mostrar el contenido del archivo
    label_contenido = tk.Label(nueva_ventana, text="Contenido del archivo:")
    label_contenido.pack(pady=10)

    # Cuadro de texto para mostrar el contenido del archivo
    text_area = tk.Text(nueva_ventana, wrap='word', height=15, width=50)
    text_area.pack(pady=10)
    text_area.insert(tk.END, contenido)  # Insertar el contenido del archivo en el cuadro de texto
    text_area.config(state=tk.DISABLED)  # Deshabilitar la edición
    #Etiqueta de campo del nombre de la base de datos
    label_nombre = tk.Label(nueva_ventana, text="Nombre:")
    label_nombre.pack(pady=5)

    # Entrada de texto para el nombre
    entry_nombre = tk.Entry(nueva_ventana)
    entry_nombre.pack(pady=5)

    # Etiqueta para el ComboBox
    label_combobox = tk.Label(nueva_ventana, text="Selecciona una opción:")
    label_combobox.pack(pady=5)

    # Opciones para el ComboBox
    opciones = [",", ";", "|"]

    # Creación del ComboBox
    combobox = ttk.Combobox(nueva_ventana, values=opciones)
    combobox.pack(pady=5)
    combobox.set("Seleccionar...")  # Valor inicial

    # Botón de enviar
    boton_enviar = tk.Button(nueva_ventana, text="Enviar", command=lambda: mostrar_datos(entry_nombre.get(), combobox.get(),nueva_ventana))
    boton_enviar.pack(pady=10)

# Función para mostrar los datos ingresados en el formulario
def mostrar_datos(nombre, opcion,nueva_ventana):
    if nombre and opcion != "Seleccionar...":
        #cierra la ventana al enviar los datos
        nueva_ventana.destroy()
        messagebox.showinfo("Datos", f"Nombre: {nombre}\nOpción seleccionada: {opcion}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

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
            abrir_nueva_ventana(content)  # Llamar a la función para abrir la nueva ventana
    else:
        print("No se seleccionó ningún archivo.")
    
    


def enviar_formulario(nombre, email, telefono):
    # Aquí puedes procesar los datos del formulario
    messagebox.showinfo("Formulario Enviado", f"Nombre: {nombre}\nCorreo Electrónico: {email}\nTeléfono: {telefono}")
