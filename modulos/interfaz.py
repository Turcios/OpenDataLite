import tkinter as tk 
from tkinter import Menu, Frame,  Toplevel, Label, Listbox, Text, ttk, Scrollbar
from modulos.base_datos import validar_bd
from modulos.idioma import obtener_texto, cambiar_idioma
from modulos.asistente import abrir_wizard, exportar_pdf
from PIL import Image, ImageTk
import modulos.file as file
import modulos.base_datos as base_datos
import modulos.variable as var


def iniciar_interface():
    root = tk.Tk()
    root.title("OpenDataLite")
    root.geometry("1000x600") 
    # Agregar el icono de OpenDataLite
    root.iconbitmap("logo.ico")
    app = InterfazApp(root)
    root.mainloop()

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.conn = None
        self.menu_import = None

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
        self.notebook.add(self.frame_consultas, text=obtener_texto('queries'))

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
        self.query_entry.insert("1.0", "--Ejemplo:\n--SELECT * FROM nombre_tabla; \n--SELECT * FROM nombre_tabla WHERE nombre_columna = valor;")
        # Exportar y ejecutar consulta
        self.boton_ejecutar = ttk.Button(self.frame_query, text=obtener_texto('execute'), command=lambda: base_datos.ejecutar_sql(self.query_entry, self.treeview, var.nombre_bd, self.root))
        self.boton_ejecutar.pack(side="right", padx=10, pady=5) 
        self.export_query_button = ttk.Button(self.frame_query, text="Exportar Consulta", command=lambda:base_datos.exportar_consulta(self.query_entry))
        self.export_query_button.pack(side="right", padx=10, pady=5)
         
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
        # Aquí se instancia el asistente como clase
        #self.asistente = AsistenteGraficos(self.frame_graficos)
        
        # Frame para resultados (Treeview, parte inferior)
        self.frame_treeview = Frame(self.frame_consultas)
        self.frame_treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Scrollbars
        self.tree_scrollbar_y = ttk.Scrollbar(self.frame_treeview, orient="vertical")
        self.tree_scrollbar_x = ttk.Scrollbar(self.frame_treeview, orient="horizontal")

        # Crear Treeview con los scrollbars configurados
        self.treeview = ttk.Treeview(
            self.frame_treeview,
            yscrollcommand=self.tree_scrollbar_y.set,
            xscrollcommand=self.tree_scrollbar_x.set
        )

        # Configurar los scrollbars para que controlen el Treeview
        self.tree_scrollbar_y.config(command=self.treeview.yview)
        self.tree_scrollbar_x.config(command=self.treeview.xview)

        # Empaquetar los widgets correctamente
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.tree_scrollbar_y.grid(row=0, column=1, sticky="ns")  # Vertical a la derecha
        self.tree_scrollbar_x.grid(row=1, column=0, sticky="ew")  # Horizontal abajo

        # Permitir que el Treeview se expanda en el frame
        self.frame_treeview.columnconfigure(0, weight=1)
        self.frame_treeview.rowconfigure(0, weight=1)

        # Exportar resultados 
        self.export_tree_button = ttk.Button(self.frame_treeview, text="Exportar Resultados", command=lambda:base_datos.exportar_resultados_csv(self))
        self.export_tree_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="e", padx=10, ipadx=10)

        #menu de importar CSV
        self.menu_import  
        
        # Crear el menú principal
        self.crear_menu() 
    
    def crear_menu(self):
        barra_menu = Menu(self.root)
        # Menú Archivos
        menu_archivo = Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label=obtener_texto('new_data_base'), command=lambda: file.nueva_archivo(self.left_panel, 2))
        menu_archivo.add_command(label=obtener_texto('menu_import_db'), command=lambda: file.cargar_base(self.left_panel,menu_import))
        menu_archivo.add_separator()
        # Submenú de Archivos
        menu_import = Menu(barra_menu, tearoff=0)
        menu_import.add_command(label=obtener_texto('CSV'), command=lambda: file.nueva_archivo(self.left_panel, 1), state='disabled') #
        menu_archivo.add_cascade(label=obtener_texto('import'), menu=menu_import)
        self.menu_import= menu_import 
        barra_menu.add_cascade(label=obtener_texto('menu_file'), menu=menu_archivo)
        
        #Menú Gráficos
        menu_consultas = Menu(barra_menu, tearoff=0)
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
        menu_ayuda.add_separator()
        menu_ayuda.add_command(label=obtener_texto('menu_exit'), command=self.root.quit)
        self.root.config(menu=barra_menu)

    def mostrar_asistente(self):
        self.notebook.select(self.frame_graficos)
        abrir_wizard(self.frame_graficos)
        
    def crear_accesos_directos(self):
        self.shortcut_bar = Frame(self.root, height=30, bg='#ddd')
        self.shortcut_bar.pack(fill='x')
        ttk.Button(self.shortcut_bar, text=obtener_texto('menu_import_db'), command=lambda: file.cargar_base(self.left_panel, self.menu_import)).pack(side='left', padx=5)
        ttk.Button(self.shortcut_bar, text=obtener_texto('menu_query_assistant'), command=lambda:self.mostrar_asistente).pack(side='left', padx=5)
    
    def mostrar_acerca_de(self):
        self.ventana = Toplevel()
        self.ventana.title("Acerca de OpenDataLite")
        self.ventana.geometry("400x500")
        self.ventana.resizable(False, False)

        # Logo
        imagen_original = Image.open("logo1.jpg")
        imagen_redimensionada = imagen_original.resize((100, 100), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(imagen_redimensionada)

        logo_label = Label(self.ventana, image=logo)
        logo_label.image = logo  # Referencia para evitar que la imagen se borre
        logo_label.pack(pady=(30, 10))

        # Texto del "Acerca de"
        texto = (
            "Proyecto de Licenciatura:\n"
            "OpenDataLite\n\n"
            "Por:\n"
            "Viviana López Turcios\n"
            "Keren Loáiciga Fallas\n\n"
            "Versión 1.0\n"
            "© 2025"
        )
        texto_label = Label(self.ventana, text=texto, font=("Segoe UI", 20), justify="center")
        texto_label.pack(padx=20, pady=10)

        # Botón de cerrar
        cerrar_btn = tk.Button(self.ventana, text="Cerrar", command=self.ventana.destroy)
        cerrar_btn.pack(pady=(20, 10))
def actualizar_textos(app):
    # Actualiza los textos del menú al cambiar de idioma.
    app.crear_menu()
    app.crear_accesos_directos()

def cambiar_idioma_y_actualizar(app, idioma):
    # Cambia el idioma y actualiza los textos del menú.
    cambiar_idioma(idioma)
    actualizar_textos(app)