import tkinter as tk
from tkinter import messagebox

# Función para mostrar un mensaje de información
def button_click():
    messagebox.showinfo("Mensaje", "¡Hola, mundo!")

# Función para establecer el ícono de la ventana
def set_window_icon(root, icon_path):
    try:
        root.iconbitmap(icon_path)
    except tk.TclError:
        messagebox.showwarning("Advertencia", "No se pudo encontrar el archivo de icono")

# Función para crear la barra de navegación superior con texto estático
def create_navbar(frame):
    navbar_frame = tk.Frame(frame)  # Crear un frame para la barra de navegación
    navbar_frame.pack(side=tk.TOP, fill=tk.X)  # Empaquetar el frame en la parte superior y que se extienda en X

    texts = ["Base de Datos", "Gráficos", ]  # Lista de textos para los elementos de la barra de navegación
    for text in texts:
        navbar_label = tk.Label(navbar_frame, text=text, padx=10, pady=5)  # Crear etiquetas con el texto deseado
        navbar_label.pack(side=tk.LEFT)  # Empaquetar etiquetas en la barra de navegación

# Función para crear la barra lateral izquierda
def create_sidebar(frame):
    sidebar_frame = tk.Frame(frame, bg='gray', width=200)  # Crear un frame para la barra lateral con ancho fijo
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)  # Empaquetar la barra lateral a la izquierda y que se extienda en Y

    sidebar_label = tk.Label(sidebar_frame, text="Barra lateral", bg='gray', fg='white', padx=10, pady=10)  # Crear etiqueta para la barra lateral
    sidebar_label.pack(fill=tk.X)  # Empaquetar etiqueta en la barra lateral

    buttons = ["Data Base", "OpenDataLite", "Tabla"]
    for text in buttons:
        sidebar_button = tk.Button(sidebar_frame, text=text, command=button_click)  # Crear botones con texto y comando asociado
        sidebar_button.pack(pady=10)  # Empaquetar botones en la barra lateral

# Función para crear el contenido principal
def create_content(frame):
    content_label = tk.Label(frame, text="Contenido principal", bg='white', padx=20, pady=20)  # Crear etiqueta para el contenido principal
    content_label.pack(fill=tk.BOTH, expand=True)  # Empaquetar etiqueta y hacerla expandible en ambas direcciones

# Función principal donde se configura la ventana principal
def main():
    root = tk.Tk()  # Crear instancia de Tkinter para la ventana principal
    root.title("OpenDataLite")  # Establecer título de la ventana
    set_window_icon(root, 'C:/Users/Katherine/Documents/ico.ico')  # Establecer ícono de la ventana

    main_frame = tk.Frame(root)  # Crear un frame principal dentro de la ventana
    main_frame.pack(fill=tk.BOTH, expand=True)  # Empaquetar el frame principal y hacerlo expandible

    navbar_frame = tk.Frame(main_frame, bg='blue')  # Crear un frame para la barra de navegación dentro del frame principal
    navbar_frame.pack(side=tk.TOP, fill=tk.X)  # Empaquetar la barra de navegación en la parte superior y que se extienda en X
    create_navbar(navbar_frame)  # Llamar función para crear la barra de navegación con texto estático

    sidebar_frame = tk.Frame(main_frame, bg='gray', width=200)  # Crear un frame para la barra lateral dentro del frame principal con ancho fijo
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)  # Empaquetar la barra lateral a la izquierda y que se extienda en Y
    create_sidebar(sidebar_frame)  # Llamar función para crear la barra lateral

    content_frame = tk.Frame(main_frame, bg='white')  # Crear un frame para el contenido principal dentro del frame principal
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Empaquetar el contenido principal a la izquierda y hacerlo expandible en ambas direcciones
    create_content(content_frame)  # Llamar función para crear el contenido principal

    root.state('zoomed')  # Maximizar la ventana al iniciar
    root.mainloop()  # Iniciar el bucle principal de eventos

if __name__ == "__main__":
    main()  # Ejecutar la función principal si el script se ejecuta directamente
