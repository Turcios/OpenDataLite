IDIOMAS = {
    'es': {
        'menu_file': 'Archivo',
        'menu_import': 'Importar',
        'menu_import_db': 'Abrir base de datos',
        'menu_import_csv': 'Nueva base de datos',
        'menu_exit': 'Salir',
        'menu_queries': 'Consultas',
        'queries_SQL':'Consulta SQL',
        'menu_generate_queries': 'Generar consultas',
        'menu_query_assistant': 'Asistente de gráficos',
        'menu_help': 'Ayuda',
        'menu_about': 'Acerca de',
        'menu_language': 'Idioma',
        'spanish': 'Español',
        'english': 'Inglés',
        'about_message': 'OpenDataLite - Herramienta para gestión de datos',
        'new_data_base': 'Nueva base de datos',
        'import':'Importar',
        'CSV':'Archivo CSV',
        'execute':'Ejecutar',
        'table_db':'Tabla en la base de datos',
        'charts':'Gráficos',
        'visualizing_charts':'Visualización de Gráficos'
    },
    'en': {
        'menu_file': 'File',
        'menu_import': 'Import',
        'menu_import_db': 'Open database',
        'menu_import_csv': 'New database',
        'menu_exit': 'Exit',
        'menu_queries': 'Queries',        
        'queries_SQL':'SQL queries',
        'menu_generate_queries': 'Generate queries',
        'menu_query_assistant': 'Query assistant',
        'menu_help': 'Help',
        'menu_about': 'About',
        'menu_language': 'Language',
        'spanish': 'Spanish',
        'english': 'English',
        'about_message': 'OpenDataLite - Data management tool',
        'new_data_base':'New Date Base',
        'import':'Import',
        'CSV':'File CSV',
        'execute':'Execute',
        'table_db':'Tables in the database',
        'charts':'Charts',
        'visualizing_charts':'Visualizing Charts'
    }
} 

idioma_actual = "es"

def obtener_texto(clave):
    return IDIOMAS.get(idioma_actual, {}).get(clave, f"[{clave}]")

def cambiar_idioma(idioma):
    global idioma_actual
    if idioma in IDIOMAS:
        idioma_actual = idioma
    else:
        raise ValueError(f"Idioma '{idioma}' no soportado.")
