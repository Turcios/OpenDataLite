IDIOMAS = {
    'es': {
        'menu_file': 'Archivo',
        'menu_import': 'Importar',
        'menu_import_db': 'Base de datos existente',
        'menu_import_csv': 'Nueva base de datos',
        'menu_exit': 'Salir',
        'menu_queries': 'Consultas',
        'menu_generate_queries': 'Generar consultas',
        'menu_query_assistant': 'Asistente de consultas',
        'menu_help': 'Ayuda',
        'menu_about': 'Acerca de',
        'menu_language': 'Idioma',
        'spanish': 'Español',
        'english': 'Inglés',
        'about_message': 'OpenDataLite - Herramienta para gestión de datos',
        'New Date Base': 'Nueva base de datos'
    },
    'en': {
        'menu_file': 'File',
        'menu_import': 'Import',
        'menu_import_db': 'Existing database',
        'menu_import_csv': 'New database',
        'menu_exit': 'Exit',
        'menu_queries': 'Queries',
        'menu_generate_queries': 'Generate queries',
        'menu_query_assistant': 'Query assistant',
        'menu_help': 'Help',
        'menu_about': 'About',
        'menu_language': 'Language',
        'spanish': 'Spanish',
        'english': 'English',
        'about_message': 'OpenDataLite - Data management tool',
        'New Date Base':'New Date Base'
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
