from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para conectar a la Base de Datos
def get_db():
    conn = sqlite3.connect('obra.db')
    return conn

# --- RUTA DE INICIO (LOGIN) ---

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form['usuario']
    pas = request.form['password']
    
    # Lógica de acceso por roles
    if user == "ingeniero" and pas == "uady":
        return redirect(url_for('panel_ingeniero'))
    elif user == "albañil" and pas == "123":
        return redirect(url_for('panel_albanil'))
    else:
        return "<h1>Error: Usuario o contraseña incorrectos</h1><a href='/'>Volver</a>"

# --- PANEL DEL INGENIERO (Gestión Total) ---

@app.route('/ingeniero')
def panel_ingeniero():
    conn = get_db()
    # Obtenemos la lista de materiales para el inventario
    materiales = conn.execute('SELECT * FROM materiales').fetchall()
    # Obtenemos el historial de salidas con nombres de materiales
    movimientos = conn.execute('''
        SELECT m.fecha, m.usuario, mat.nombre, m.cantidad_sacada 
        FROM movimientos m 
        JOIN materiales mat ON m.material_id = mat.id
        ORDER BY m.fecha DESC
    ''').fetchall()
    conn.close()
    return render_template('ingeniero.html', materiales=materiales, movimientos=movimientos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cant = request.form['cantidad']
    unid = request.form['unidad']
    
    conn = get_db()
    conn.execute('INSERT INTO materiales (nombre, cantidad, unidad) VALUES (?, ?, ?)', (nombre, cant, unid))
    conn.commit()
    conn.close()
    return redirect(url_for('panel_ingeniero'))

# --- PANEL DEL ALBAÑIL (Vista de Stock y Solicitud) ---

@app.route('/albañil')
def panel_albanil():
    conn = get_db()
    # Traemos los materiales para que el albañil los vea en su lista desplegable
    materiales = conn.execute('SELECT * FROM materiales').fetchall()
    conn.close()
    return render_template('albanil.html', materiales=materiales)

@app.route('/sacar', methods=['POST'])
def sacar():
    mat_id = request.form['material_id']
    cant = int(request.form['cantidad'])
    user = request.form['usuario']
    
    conn = get_db()
    # Verificamos si hay stock suficiente
    res = conn.execute('SELECT cantidad, nombre FROM materiales WHERE id=?', (mat_id,)).fetchone()
    
    if res and res[0] >= cant:
        # Restamos la cantidad del inventario
        conn.execute('UPDATE materiales SET cantidad = cantidad - ? WHERE id=?', (cant, mat_id))
        # Registramos quién se llevó el material
        conn.execute('INSERT INTO movimientos (usuario, material_id, cantidad_sacada) VALUES (?, ?, ?)', (user, mat_id, cant))
        conn.commit()
        conn.close()
        return f"<h1>✅ Solicitud Registrada</h1><p>Se han descontado {cant} unidades de {res[1]}.</p><a href='/albañil'>Volver al panel</a>"
    else:
        conn.close()
        return f"<h1>❌ Error de Stock</h1><p>No hay suficiente {res[1] if res else 'material'} disponible.</p><a href='/albañil'>Volver a intentar</a>"

if __name__ == '__main__':
    app.run(debug=True)
