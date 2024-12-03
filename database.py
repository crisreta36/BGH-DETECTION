import sqlite3

def crear_bd():
    conn = sqlite3.connect('bgh_powercheck.db')
    cursor = conn.cursor()

    # Crear la tabla de registros
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros
                      (id INTEGER PRIMARY KEY, tipo TEXT, fecha TEXT)''')
    conn.commit()
    conn.close()

def registrar(tipo):
    conn = sqlite3.connect('bgh_powercheck.db')
    cursor = conn.cursor()

    # Registrar un evento (correcto o fallido)
    cursor.execute("INSERT INTO registros (tipo, fecha) VALUES (?, datetime('now'))", (tipo,))
    conn.commit()
    conn.close()

def mostrar_fallidos():
    conn = sqlite3.connect('bgh_powercheck.db')
    cursor = conn.cursor()

    # Obtener registros fallidos
    cursor.execute("SELECT * FROM registros WHERE tipo = 'fallido'")
    fallidos = cursor.fetchall()
    for registro in fallidos:
        print(registro)
    conn.close()

def mostrar_correctos():
    conn = sqlite3.connect('bgh_powercheck.db')
    cursor = conn.cursor()

    # Obtener registros correctos
    cursor.execute("SELECT * FROM registros WHERE tipo = 'correcto'")
    correctos = cursor.fetchall()
    for registro in correctos:
        print(registro)
    conn.close()
