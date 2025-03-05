
import tkinter as tk
from tkinter import Menu, messagebox, Frame, Label, Listbox, Text, END
from modulos.base_datos import validar_bd
from modulos.idioma import obtener_texto, cambiar_idioma
from modulos.asistente import abrir_wizard, exportar_pdf
import modulos.file as file
import os

def iniciar_interface():
    # Inicia la interfaz principal de la aplicación
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

        # Frame principal
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        # Panel izquierdo (para mostrar tablas o bases de datos)
        self.left_panel = Frame(self.main_frame, width=200)
        self.left_panel.pack(side='left', fill='y')

        Label(self.left_panel, text="Tablas en la base de datos").pack()
        self.table_listbox = Listbox(self.left_panel)
        self.table_listbox.pack(fill='y', expand=True)

        # Panel derecho (para consultas y asistente)
        self.right_panel = Frame(self.main_frame)
        self.right_panel.pack(side='right', fill='both', expand=True)

        Label(self.right_panel, text="Consulta SQL").pack()
        self.query_entry = Text(self.right_panel, height=5)
        self.query_entry.pack(fill='x')

        # Resultado de consultas
        self.result_text = Text(self.right_panel)
        self.result_text.pack(fill='both', expand=True)
        

        # Frame para el Treeview y la scrollbar
        #self.frame_treeview = Frame(self.right_panel)
        #self.frame_treeview.pack(expand=True, fill='both', padx=100, pady=10)

        # Crear Treeview para mostrar los resultados de la consulta SQL
        #self.treeview = ttk.Treeview(self.frame_treeview)
        #self.treeview.pack(side="left", expand=True, fill='both')

        # Agregar una barra de desplazamiento vertical
        #self.scrollbar = ttk.Scrollbar(self.frame_treeview, orient="vertical", command=self.treeview.yview)
        #self.treeview.configure(yscroll=self.scrollbar.set)
        #self.scrollbar.pack(side="right", fill="y")

    def crear_menu(self):
        # Crea el menú principal de la aplicación con sus submenús
        barra_menu = Menu(self.root)

        # Menú Archivo
        menu_archivo = Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label=obtener_texto('menu_import_db'), command=lambda: file.nueva_archivo(self.left_panel, 1))
        menu_archivo.add_separator()  # Separador visual entre opciones
        menu_archivo.add_command(label=obtener_texto('New Date Base'), command=lambda: file.nueva_archivo(self.left_panel, 2))
        menu_archivo.add_separator()
        menu_archivo.add_command(label=obtener_texto('menu_exit'), command=self.root.quit)
        barra_menu.add_cascade(label=obtener_texto('menu_file'), menu=menu_archivo)

        # Menú Consultas
        menu_consultas = Menu(barra_menu, tearoff=0)
        menu_consultas.add_command(label=obtener_texto('menu_generate_queries'), command=lambda: validar_bd(self))
        menu_consultas.add_command(label=obtener_texto('menu_query_assistant'), command=self.mostrar_asistente)
        # Botón para exportar gráfico a PDF
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

        # Configurar el menú en la ventana principal
        self.root.config(menu=barra_menu)

    def actualizar_panel_tablas(self):
        # Limpiar el panel de tablas y mostrar las bases de datos locales (.db)
        self.table_listbox.delete(0, tk.END)
        bases_de_datos = [archivo for archivo in os.listdir('.') if archivo.endswith('.db')]
        if not bases_de_datos:
            self.table_listbox.insert(tk.END, 'No hay bases de datos disponibles')
        else:
            for archivo in bases_de_datos:
                self.table_listbox.insert(tk.END, archivo)

    def mostrar_asistente(self):
        # Mostrar el asistente en el panel derecho
        self.result_text.delete("1.0", END)
        self.result_text.insert(END, "Asistente de consultas activado...")
        abrir_wizard(self.right_panel)

    def mostrar_acerca_de(self):
        # Muestra información acerca de la aplicación
        messagebox.showinfo("Acerca de", "OpenDataLite\nVersión 1.0\n© 2025")
        
    


def actualizar_textos(app):
    # Actualiza los textos del menú al cambiar de idioma.
    app.crear_menu()

def cambiar_idioma_y_actualizar(app, idioma):
    # Cambia el idioma y actualiza los textos del menú.
    cambiar_idioma(idioma)
    actualizar_textos(app)
