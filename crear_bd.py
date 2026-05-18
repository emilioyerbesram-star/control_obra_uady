import sqlite3

conn = sqlite3.connect('obra.db')
cursor = conn.cursor()

# Crear tabla de materiales si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS materiales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cantidad REAL NOT NULL,
    unidad TEXT NOT NULL
)
''')

# Crear tabla de historial si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material TEXT NOT NULL,
    cantidad REAL NOT NULL,
    usuario TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("¡Base de datos y tablas creadas correctamente!")
