import tkinter as tk
from tkinter import messagebox, filedialog, ttk, Label
import pandas as pd
import sqlite3 
import modulos.variable as var
import csv
from modulos.idioma import obtener_texto
from PIL import Image, ImageTk

# Contexto para almacenar rutas y configuraciones actuales
db_context = {"nombre_bd": None, "nombre_tabla": None,"ruta_csv": None}

def select_archivo(tipo_archivo):
    tipos = {
        1: (obtener_texto("sqlite_file"), "*.db"),
        2: (obtener_texto("csv_file"), "*.csv")
    }
    ruta_archivo = filedialog.askopenfilename(
        title=f"{obtener_texto('select')} {tipos[tipo_archivo][0]}",
        filetypes=[tipos[tipo_archivo]]
    )
    if ruta_archivo:
        if tipo_archivo == 1:
            var.ruta_bd = ruta_archivo
        else:
            db_context["ruta_csv"] = ruta_archivo
    else:
        messagebox.showwarning(
            obtener_texto("warning"),
            f"{obtener_texto('no_select')} {tipos[tipo_archivo][0].lower()}."
        )

def abrir_nueva_ventana(frame_izquierdo):
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("OpenDataLite")
    nueva_ventana.geometry("600x400+300+200")
    nueva_ventana.transient(nueva_ventana.master)
    nueva_ventana.grab_set()
    nueva_ventana.iconbitmap("logo.ico")

    entradas = {
        obtener_texto("bd_name"): tk.Entry(nueva_ventana),
        obtener_texto("table_name"): tk.Entry(nueva_ventana)
    }
    for label_text, entry in entradas.items():
        tk.Label(nueva_ventana, text=label_text).pack(pady=5)
        entry.pack(pady=5)

    tk.Button(nueva_ventana, text=obtener_texto("csv_select"),
              command=lambda: select_archivo(2)).pack(pady=5)

    tk.Button(
        nueva_ventana, text=obtener_texto("send"),
        command=lambda: mostrar_datos(
            entradas[obtener_texto("bd_name")].get(),
            entradas[obtener_texto("table_name")].get(),
            frame_izquierdo, nueva_ventana)
    ).pack(pady=10)

def mostrar_datos(nombre_bd, nombre_tabla, frame_izquierdo, nueva_ventana):
    if not db_context.get("ruta_csv"):
        messagebox.showerror(obtener_texto("error"), obtener_texto("csv_no_seleccionado"))
        return

    try:
        df = pd.read_csv(db_context["ruta_csv"], on_bad_lines='skip')
        conexion = sqlite3.connect(nombre_bd + ".db")

        with open(db_context["ruta_csv"], 'r', encoding='utf-8') as file:
            sample = file.read(2048)
            dialect = csv.Sniffer().sniff(sample, delimiters="-,/.\t")
            file.seek(0)

        chunksize = 100000
        for chunk in pd.read_csv(db_context["ruta_csv"], delimiter=dialect.delimiter, on_bad_lines='skip', chunksize=chunksize):
            chunk.to_sql(nombre_tabla, conexion, if_exists='append', index=False)

        conexion.close()
        messagebox.showinfo(obtener_texto("success"), obtener_texto("csv_uploaded_successfully"))
        mostrar_estructura(nombre_bd + ".db", frame_izquierdo)
        db_context.update({"nombre_bd": nombre_bd + ".db", "nombre_tabla": nombre_tabla})
    except Exception as e:
        messagebox.showerror(obtener_texto("error"), f"{obtener_texto('error_csv')}: {e}")
    finally:
        nueva_ventana.destroy()

def cargar_csv_bd(frame_izquierdo, nombre_tabla, ventana_carga):
    try:
        conexion = sqlite3.connect(var.ruta_bd)
        with open(db_context["ruta_csv"], 'r', encoding='utf-8') as file:
            sample = file.read(2048)
            dialect = csv.Sniffer().sniff(sample, delimiters=",/.–\t")
            file.seek(0)

        chunksize = 100000
        for chunk in pd.read_csv(db_context["ruta_csv"], delimiter=dialect.delimiter, on_bad_lines='skip', chunksize=chunksize):
            chunk.to_sql(nombre_tabla, conexion, if_exists='append', index=False)

        conexion.close()
        mostrar_estructura(var.ruta_bd, frame_izquierdo)
        messagebox.showinfo(obtener_texto("success"), obtener_texto("data_added"))
    except Exception as e:
        messagebox.showerror(obtener_texto("error"), f"{obtener_texto('error_load_csv_db')}: {e}")
    finally:
        ventana_carga.destroy()

def cargar_base(frame_izquierdo, menu):
    archivo = filedialog.askopenfilename(
        title=obtener_texto("select_sqlite"),
        filetypes=[("SQLite files", "*.sqlite *.db"), (obtener_texto("all_files"), "*.*")]
    )
    if archivo:
        try:
            var.ruta_bd = archivo
            conexion = sqlite3.connect(var.ruta_bd)
            conexion.close()
            mostrar_estructura(var.ruta_bd, frame_izquierdo)
            menu.entryconfig(obtener_texto('CSV'), state='normal')
            messagebox.showinfo(obtener_texto("success"), obtener_texto("bd_loaded"))
        except Exception as e:
            messagebox.showerror(obtener_texto("error"), f"{obtener_texto('error_load_db')}: {e}")

def cargar_csv(frame_izquierdo):
    ventana_carga = tk.Toplevel()
    ventana_carga.title("OpenDataLite")
    ventana_carga.geometry("600x400+300+200")
    ventana_carga.iconbitmap("logo.ico")
    ventana_carga.transient(ventana_carga.master)
    ventana_carga.grab_set()

    tk.Button(ventana_carga, text=obtener_texto("csv_select"), command=lambda: select_archivo(2)).pack(pady=5)

    label_nombre_tabla = tk.Label(ventana_carga, text=obtener_texto("table_name"))
    label_nombre_tabla.pack(pady=5)
    entry_nombre_tabla = tk.Entry(ventana_carga)
    entry_nombre_tabla.pack(pady=5)

    tk.Button(
        ventana_carga, text=obtener_texto("send"),
        command=lambda: cargar_csv_bd(frame_izquierdo, entry_nombre_tabla.get(), ventana_carga)
    ).pack(pady=10)

def mostrar_estructura(nombre_bd, frame_izquierdo):
    for widget in frame_izquierdo.winfo_children():
        widget.destroy()

    tk.Label(frame_izquierdo, text=f"{obtener_texto('structure')} {nombre_bd}").pack(pady=5)

    treeview = ttk.Treeview(frame_izquierdo)
    treeview.pack(expand=True, fill="both", padx=10, pady=10)
    treeview.heading("#0", text=obtener_texto("table"), anchor="w")

    try:
        var.nombre_bd = nombre_bd
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for tabla in cursor.fetchall():
            nombre_tabla = tabla[0]
            nodo_tabla = treeview.insert("", "end", text=nombre_tabla, open=False)
            cursor.execute(f"PRAGMA table_info('{nombre_tabla}');")
            for columna in cursor.fetchall():
                treeview.insert(nodo_tabla, "end", text=columna[1], open=False)
    finally:
        conexion.close()

def nueva_archivo(frame_izquierdo, tipo):
    if tipo == 1:
        cargar_csv(frame_izquierdo)
    elif tipo == 2:
        abrir_nueva_ventana(frame_izquierdo)


