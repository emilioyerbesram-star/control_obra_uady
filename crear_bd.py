import sqlite3

conn = sqlite3.connect('obra.db')
cursor = conn.cursor()

# Creamos la tabla de materiales
cursor.execute('''
    CREATE TABLE IF NOT EXISTS materiales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        unidad TEXT NOT NULL
    )
''')

# Creamos la tabla de movimientos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        material_id INTEGER,
        cantidad_sacada INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(material_id) REFERENCES materiales(id)
    )
''')

conn.commit()
conn.close()
print("¡Tablas creadas con éxito en obra.db!")