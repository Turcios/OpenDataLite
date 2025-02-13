
import tkinter as tk
from tkinter import Menu, messagebox, filedialog, Frame, Label, Listbox, Text, END
from modulos.base_datos import obtener_tablas_bd, ejecutar_consulta, conectar_bd
from modulos.idioma import obtener_texto, cambiar_idioma
from modulos.asistente import abrir_wizard, exportar_pdf
import sqlite3
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
        self.base_datos_actual = None

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

        # Botón para exportar gráfico a PDF
        self.exportar_pdf_btn = tk.Button(self.right_panel, text="Exportar Gráfico a PDF", command=exportar_pdf)
        self.exportar_pdf_btn.pack()

        Label(self.right_panel, text="Consulta SQL").pack()
        self.query_entry = Text(self.right_panel, height=5)
        self.query_entry.pack(fill='x')

        # Resultado de consultas
        self.result_text = Text(self.right_panel)
        self.result_text.pack(fill='both', expand=True)

    def crear_menu(self):
        # Crea el menú principal de la aplicación con sus submenús
        barra_menu = Menu(self.root)

        # Menú Archivo
        menu_archivo = Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label=obtener_texto('menu_import_db'), command=self.cargar_base_datos)
        menu_archivo.add_separator()  # Separador visual entre opciones
        menu_archivo.add_command(label=obtener_texto('New Date Base'), command=self.crear_nueva_base_datos)
        menu_archivo.add_separator()
        menu_archivo.add_command(label=obtener_texto('menu_exit'), command=self.root.quit)
        barra_menu.add_cascade(label=obtener_texto('menu_file'), menu=menu_archivo)

        # Menú Consultas
        menu_consultas = Menu(barra_menu, tearoff=0)
        menu_consultas.add_command(label=obtener_texto('menu_generate_queries'), command=self.ejecutar_consulta)
        menu_consultas.add_command(label=obtener_texto('menu_query_assistant'), command=self.mostrar_asistente)
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

    def cargar_base_datos(self):
        ruta_bd = filedialog.askopenfilename(title="Seleccionar base de datos", filetypes=[("Archivos SQLite", "*.db")])
        if ruta_bd:
            try:
                self.conn = conectar_bd(ruta_bd)
                self.base_datos_actual = ruta_bd
                messagebox.showinfo("Éxito", "Base de datos cargada correctamente")
                self.mostrar_tablas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la base de datos: {str(e)}")

    def crear_nueva_base_datos(self):
        # Crear una ventana emergente para crear una nueva base de datos
        self.ventana_nueva_bd = tk.Toplevel(self.root)
        self.ventana_nueva_bd.title('Nueva Base de Datos')
        self.ventana_nueva_bd.geometry('500x400')

        # Campo para el nombre de la base de datos
        tk.Label(self.ventana_nueva_bd, text='Nombre base de datos').pack(pady=5)
        self.nombre_bd_entry = tk.Entry(self.ventana_nueva_bd)
        self.nombre_bd_entry.pack(pady=5)

        # Campo para el nombre de la tabla
        tk.Label(self.ventana_nueva_bd, text='Nombre de la tabla').pack(pady=5)
        self.nombre_tabla_entry = tk.Entry(self.ventana_nueva_bd)
        self.nombre_tabla_entry.pack(pady=5)

        # Botón para seleccionar el archivo CSV
        tk.Label(self.ventana_nueva_bd, text='Base de archivo CSV:').pack(pady=5)
        self.archivo_csv_btn = tk.Button(self.ventana_nueva_bd, text='Seleccionar archivo CSV', command=self.seleccionar_archivo_csv)
        self.archivo_csv_btn.pack(pady=5)

        # Botón para enviar
        self.enviar_btn = tk.Button(self.ventana_nueva_bd, text='Enviar', command=self.cargar_nueva_base_datos)
        self.enviar_btn.pack(pady=10)

    def seleccionar_archivo_csv(self):
        # Mantener la ventana emergente al frente
        self.ventana_nueva_bd.attributes('-topmost', True)
        self.ruta_csv = filedialog.askopenfilename(filetypes=[('Archivos CSV', '*.csv')])
        # self.ventana_nueva_bd.attributes('-topmost', False)  # Opcional: restablecer la propiedad
        if self.ruta_csv:
            messagebox.showinfo('Archivo Seleccionado', f'Se seleccionó: {self.ruta_csv}')

    def cargar_nueva_base_datos(self):
        nombre_bd = self.nombre_bd_entry.get()
        nombre_tabla = self.nombre_tabla_entry.get()

        if not nombre_bd or not nombre_tabla or not hasattr(self, 'ruta_csv'):
            messagebox.showerror('Error', 'Todos los campos son obligatorios')
            return
        # Crear la base de datos y cargar el CSV
        try:
            conexion = sqlite3.connect(f'{nombre_bd}.db')
            cursor = conexion.cursor()
            # Crear la tabla
            cursor.execute(f'CREATE TABLE {nombre_tabla} (id INTEGER PRIMARY KEY AUTOINCREMENT, datos TEXT)')
            # Leer y cargar datos del CSV
            with open(self.ruta_csv, 'r') as archivo:
                for linea in archivo:
                    cursor.execute(f'INSERT INTO {nombre_tabla} (datos) VALUES (?)', (linea.strip(),))
            conexion.commit()
            messagebox.showinfo('Éxito', 'Base de datos creada y datos cargados correctamente')
            
            # Actualizar la base de datos actual
            self.base_datos_actual = f'{nombre_bd}.db'
            self.mostrar_tablas()  # Actualizar el panel de tablas
            self.ventana_nueva_bd.destroy()  # Cerrar la ventana emergente
        except Exception as e:
            messagebox.showerror('Error', f'Ocurrió un error: {e}')
        finally:
            conexion.close()

    def actualizar_panel_tablas(self):
        # Limpiar el panel de tablas y mostrar las bases de datos locales (.db)
        self.table_listbox.delete(0, tk.END)
        bases_de_datos = [archivo for archivo in os.listdir('.') if archivo.endswith('.db')]
        if not bases_de_datos:
            self.table_listbox.insert(tk.END, 'No hay bases de datos disponibles')
        else:
            for archivo in bases_de_datos:
                self.table_listbox.insert(tk.END, archivo)

    def mostrar_tablas(self):
        if not self.base_datos_actual:
            messagebox.showerror("Error", "No hay una base de datos cargada")
            return

        self.table_listbox.delete(0, END)
        tablas = obtener_tablas_bd(self.base_datos_actual)
        for tabla in tablas:
            self.table_listbox.insert(END, tabla)

    def ejecutar_consulta(self):
        if not self.base_datos_actual:
            messagebox.showerror("Error", "No hay una base de datos cargada")
            return

        query = self.query_entry.get("1.0", END).strip()
        if not query:
            messagebox.showwarning("Advertencia", "La consulta SQL está vacía")
            return 

        try:
            resultados = ejecutar_consulta(query, self.base_datos_actual)
            self.result_text.delete("1.0", END)
            for fila in resultados:
                self.result_text.insert(END, f"{fila}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar la consulta: {str(e)}")

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
