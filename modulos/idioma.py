IDIOMAS = {
    'es': {
        'menu_file': 'Archivo',
        'menu_import': 'Importar',
        'menu_import_db': 'Abrir base de datos',
        'menu_import_csv': 'Nueva base de datos',
        'menu_exit': 'Salir',
        'menu_queries': 'Gráficos',
        'queries':'Consulta',
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
        'visualizing_charts':'Visualización de Gráficos',
        'sucess':'Éxito','select_db_title': 'Seleccionar base de datos',
        'warning': 'Advertencia',
        'warning_no_db_selected': 'No se seleccionó ninguna base de datos.',
        'error_title': 'Error',
        'error_no_db': 'No hay una base de datos cargada',
        'query_empty': 'La consulta SQL está vacía',
        'query_success': 'Consulta ejecutada exitosamente.',
        'no_results': 'No se encontró resultado de la consulta',
        'loading_title': 'Cargando',
        'executing_query': 'Ejecutando consulta, por favor espere...',
        'sql_error': 'Error de SQL',
        'sql_query_error': 'Error en la consulta SQL',
        'export_success': 'Consulta exportada correctamente.',
        'no_valid_query': 'No hay consulta válida para exportar.',
        'no_export_data': 'No hay resultados para exportar.',
        'index': 'Índice'
    },
    'en': {
        'menu_file': 'File',
        'menu_import': 'Import',
        'menu_import_db': 'Open database',
        'menu_import_csv': 'New database',
        'menu_exit': 'Exit',
        'menu_queries': 'Grafic',        
        'queries_SQL':'SQL queries',
        'queries':'Querie',
        'menu_generate_queries': 'Generate queries',
        'menu_query_assistant': 'Grafic wizard',
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
        'visualizing_charts':'Visualizing Charts',
        'sucess':'Éxito',
        'select_db_title': 'Select Database',
        'warning_title': 'Warning',
        'warning_no_db_selected': 'No database was selected.',
        'error_title': 'Error',
        'error_no_db': 'There is no database currently loaded.',
        'query_empty': 'The SQL query is empty.',
        'query_success': 'Query executed successfully.',
        'no_results': 'No results found from the query.',
        'loading_title': 'Loading',
        'executing_query': 'Executing query, please wait...',
        'sql_error': 'SQL Error',
        'sql_query_error': 'An error occurred in the SQL query',
        'export_success': 'Query exported successfully.',
        'no_valid_query': 'There is no valid query to export.',
        'no_export_data': 'There are no results to export.',
        'index': 'Index'
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
