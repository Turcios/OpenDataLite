import tkinter as tk 
from tkinter import Menu, messagebox, Frame, Label, Listbox, Text, END, ttk
from modulos.base_datos import validar_bd
from modulos.idioma import obtener_texto, cambiar_idioma
from modulos.asistente import abrir_wizard, exportar_pdf
import modulos.file as file
import os

def iniciar_interface():
    root = tk.Tk()
    root.title("OpenDataLite")
    root.geometry("1000x600")
    app = InterfazApp(root)
    root.mainloop()

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.conn = None

        # Crear el menú principal
        self.crear_menu()

        # Barra de accesos directos
        self.crear_accesos_directos()

        # Frame principal
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        # Panel izquierdo (Lista de tablas de la BD)
        self.left_panel = Frame(self.main_frame, width=200)
        self.left_panel.pack(side='left', fill='y')
        Label(self.left_panel, text="Tablas en la base de datos").pack()
        self.table_listbox = Listbox(self.left_panel)
        self.table_listbox.pack(fill='y', expand=True)

        # Pestañas en el panel derecho
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(side='right', fill='both', expand=True)
      
        # Pestaña de Consultas
        self.frame_consultas = Frame(self.notebook)
        self.notebook.add(self.frame_consultas, text='Consultas')
        Label(self.frame_consultas, text="Consulta SQL").pack()
        self.query_entry = Text(self.frame_consultas, height=5)
        self.query_entry.pack(fill='x')
        self.result_text = Text(self.frame_consultas)
        self.result_text.pack(fill='both', expand=True)

        # Pestaña de Gráficos
        self.frame_graficos = Frame(self.notebook)
        self.notebook.add(self.frame_graficos, text='Gráficos')
        Label(self.frame_graficos, text="Visualización de Gráficos").pack()

    def crear_menu(self):
        barra_menu = Menu(self.root)
         # Menú Archivos
        menu_archivo = Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label=obtener_texto('new_data_base'), command=lambda: file.nueva_archivo(self.left_panel, 2))
        menu_archivo.add_command(label=obtener_texto('menu_import_db'), command=lambda: file.nueva_archivo(self.left_panel, self.menu_import))
         # Submenú de Archivos
        menu_import = Menu(barra_menu, tearoff=0)
        menu_import.add_command(label=obtener_texto('CSV'), command=lambda: file.nueva_archivo(self.left_panel, 1)) #, state='disabled'
        menu_archivo.add_cascade(label=obtener_texto('import'), menu=menu_import)
        #menu_archivo.add_separator()
        barra_menu.add_cascade(label=obtener_texto('menu_file'), menu=menu_archivo)
        
        #Menú Consultas
        menu_consultas = Menu(barra_menu, tearoff=0)
        menu_consultas.add_command(label=obtener_texto('menu_generate_queries'), command=lambda: validar_bd(self))
        menu_consultas.add_command(label=obtener_texto('menu_query_assistant'), command=self.mostrar_asistente)
        menu_consultas.add_command(label="Exportar Gráfico a PDF", command=exportar_pdf)
        barra_menu.add_cascade(label=obtener_texto('menu_queries'), menu=menu_consultas)
        
        # Menú Ayuda
        menu_ayuda = Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label=obtener_texto('menu_about'), command=self.mostrar_acerca_de)

        # Submenú de Idioma
        menu_idioma = Menu(menu_ayuda, tearoff=0)
        menu_idioma.add_command(label=obtener_texto('spanish'),
                                command=lambda: cambiar_idioma_y_actualizar(self, 'es'))
        menu_idioma.add_command(label=obtener_texto('english'),
                                command=lambda: cambiar_idioma_y_actualizar(self, 'en'))
        menu_ayuda.add_cascade(label=obtener_texto('menu_language'), menu=menu_idioma)

        barra_menu.add_cascade(label=obtener_texto('menu_help'), menu=menu_ayuda)

        menu_ayuda.add_command(label=obtener_texto('menu_exit'), command=self.root.quit)
        self.root.config(menu=barra_menu)
    
    def crear_accesos_directos(self):
        self.shortcut_bar = Frame(self.root, height=30, bg='#ddd')
        self.shortcut_bar.pack(fill='x')
        ttk.Button(self.shortcut_bar, text="Abrir", command=lambda: file.nueva_archivo(self.left_panel, 3)).pack(side='left', padx=5)
        ttk.Button(self.shortcut_bar, text="Ejecutar", command=lambda: validar_bd(self)) .pack(side='left', padx=5)
    
    def mostrar_asistente(self):
        self.result_text.delete("1.0", END)
        self.result_text.insert(END, "Asistente de consultas activado...")
        abrir_wizard(self.frame_consultas)
    
    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "OpenDataLite\nVersión 1.0\n© 2025")

def actualizar_textos(app):
    # Actualiza los textos del menú al cambiar de idioma.
    app.crear_menu()

def cambiar_idioma_y_actualizar(app, idioma):
    # Cambia el idioma y actualiza los textos del menú.
    cambiar_idioma(idioma)
    actualizar_textos(app)
