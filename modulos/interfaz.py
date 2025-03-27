import tkinter as tk 
from tkinter import Menu, messagebox, Frame, Label, Listbox, Text, ttk, Scrollbar
from modulos.base_datos import validar_bd
from modulos.idioma import obtener_texto, cambiar_idioma
from modulos.asistente import abrir_wizard, exportar_pdf
import modulos.file as file
import modulos.base_datos as base_datos
import modulos.variable as var


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
        Label(self.left_panel, text=obtener_texto('table_db')).pack()
        self.table_listbox = Listbox(self.left_panel)
        self.table_listbox.pack(fill='y', expand=True)

        # Pestañas en el panel derecho
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(side='right', fill='both', expand=True)
      
        # Pestaña de Consultas
        self.frame_consultas = Frame(self.notebook)
        self.notebook.add(self.frame_consultas, text=obtener_texto('menu_queries'))

        # Configurar el layout con grid
        self.frame_consultas.columnconfigure(0, weight=1)
        self.frame_consultas.rowconfigure(1, weight=1)  # Para que el frame de resultados expanda

        # Frame para la entrada de consulta (Parte superior)
        self.frame_query = Frame(self.frame_consultas)
        self.frame_query.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        Label(self.frame_query, text=obtener_texto('queries_SQL')).pack(anchor="w")

        # Frame para la entrada de consulta con scrollbar
        self.query_text_frame = Frame(self.frame_query)
        self.query_text_frame.pack(fill='x')

        # Scrollbar para la consulta SQL
        self.query_scrollbar = Scrollbar(self.query_text_frame, orient="vertical")
        self.query_entry = Text(self.query_text_frame, height=5, yscrollcommand=self.query_scrollbar.set)
        self.query_scrollbar.config(command=self.query_entry.yview)

        self.query_entry.pack(side="left", fill='both', expand=True)
        self.query_scrollbar.pack(side="right", fill="y")

        # Frame para resultados (Treeview, parte inferior)
        self.frame_treeview = Frame(self.frame_consultas)
        self.frame_treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Configurar expansión del frame_treeview
        self.frame_consultas.rowconfigure(1, weight=1)

        # Crear Treeview para mostrar los resultados de la consulta SQL
        self.treeview = ttk.Treeview(self.frame_treeview)
        self.treeview.pack(side="left", expand=True, fill='both')

        # Agregar una barra de desplazamiento vertical
        self.tree_scrollbar = ttk.Scrollbar(self.frame_treeview, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscroll=self.tree_scrollbar.set)
        self.tree_scrollbar.pack(side="right", fill="y")

        # Pestaña de Gráficos
        self.frame_graficos = Frame(self.notebook)
        self.notebook.add(self.frame_graficos, text=obtener_texto('charts')) 
        Label(self.frame_graficos, text=obtener_texto('visualizing_charts')).pack()
        
        #menu de importar CSV
        self.menu_import    
    
    def crear_menu(self):
        barra_menu = Menu(self.root)
        # Menú Archivos
        menu_archivo = Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label=obtener_texto('new_data_base'), command=lambda: file.nueva_archivo(self.left_panel, 2))
        menu_archivo.add_command(label=obtener_texto('menu_import_db'), command=lambda: file.cargar_base(self.left_panel,menu_import))
        # Submenú de Archivos
        menu_import = Menu(barra_menu, tearoff=0)
        menu_import.add_command(label=obtener_texto('CSV'), command=lambda: file.nueva_archivo(self.left_panel, 1), state='disabled') #
        menu_archivo.add_cascade(label=obtener_texto('import'), menu=menu_import)
        self.menu_import= menu_import 
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
        ttk.Button(self.shortcut_bar, text=obtener_texto('menu_import_db'), command=lambda: file.cargar_base(self.left_panel, self.menu_import)).pack(side='left', padx=5)
        self.boton_ejecutar = ttk.Button(self.shortcut_bar, text=obtener_texto('execute'), command=lambda: base_datos.ejecutar_sql(self.query_entry, self.treeview, var.nombre_bd))
        self.boton_ejecutar.pack(side='left', padx=5)
    
    def mostrar_asistente(self):
        self.notebook.select(self.frame_graficos)
        abrir_wizard(self.frame_graficos)
    
    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "OpenDataLite\nVersión 1.0\n© 2025")

def actualizar_textos(app):
    # Actualiza los textos del menú al cambiar de idioma.
    app.crear_menu()
    app.crear_accesos_directos()

def cambiar_idioma_y_actualizar(app, idioma):
    # Cambia el idioma y actualiza los textos del menú.
    cambiar_idioma(idioma)
    actualizar_textos(app)
    
