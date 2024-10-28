import sqlite3

def ejecutar_consulta(sentencia_sql):
    with sqlite3.connect("prueba.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute(sentencia_sql)
        resultado = cursor.fetchall()
        return resultado