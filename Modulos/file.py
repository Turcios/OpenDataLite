import tkinter as tk
from tkinter import messagebox

def nueva_archivo():
    # Crear un nuevo marco para el formulario
    formulario_frame = tk.Frame()
    formulario_frame.pack(pady=20)

    # Etiqueta y entrada para el campo "Nombre"
    nombre_label = tk.Label(formulario_frame, text="Nombre:")
    nombre_label.grid(row=0, column=0, padx=10, pady=5)
    nombre_entry = tk.Entry(formulario_frame)
    nombre_entry.grid(row=0, column=1, padx=10, pady=5)

    # Etiqueta y entrada para el campo "Correo Electrónico"
    email_label = tk.Label(formulario_frame, text="Correo Electrónico:")
    email_label.grid(row=1, column=0, padx=10, pady=5)
    email_entry = tk.Entry(formulario_frame)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    # Etiqueta y entrada para el campo "Teléfono"
    telefono_label = tk.Label(formulario_frame, text="Teléfono:")
    telefono_label.grid(row=2, column=0, padx=10, pady=5)
    telefono_entry = tk.Entry(formulario_frame)
    telefono_entry.grid(row=2, column=1, padx=10, pady=5)

    # Botón para enviar el formulario
    submit_button = tk.Button(formulario_frame, text="Enviar", command=lambda: enviar_formulario(nombre_entry.get(), email_entry.get(), telefono_entry.get()))
    submit_button.grid(row=3, columnspan=2, pady=10)

def enviar_formulario(nombre, email, telefono):
    # Aquí puedes procesar los datos del formulario
    messagebox.showinfo("Formulario Enviado", f"Nombre: {nombre}\nCorreo Electrónico: {email}\nTeléfono: {telefono}")
