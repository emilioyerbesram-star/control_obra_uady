from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('obra.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form['usuario']
    pas = request.form['password']
    
    if user.lower() == "ingeniero" and pas == "uady":
        return redirect(url_for('panel_ingeniero'))
    elif user.lower() == "albañil" and pas == "123":
        return redirect(url_for('panel_albanil'))
    else:
        return "<h1>❌ Error: Usuario o contraseña incorrectos</h1><br><a href='/'>Volver a intentar</a>"

@app.route('/ingeniero')
def panel_ingeniero():
    try:
        conn = get_db()
        materiales = conn.execute('SELECT * FROM materiales').fetchall()
        historial = conn.execute('SELECT * FROM historial ORDER BY fecha DESC').fetchall()
        conn.close()
        return render_template('ingeniero.html', materiales=materiales, historial=historial)
    except Exception as e:
        return f"<h1>❌ Error en Base de Datos (Ingeniero)</h1><p>{str(e)}</p>"

@app.route('/albanil_panel')
def panel_albanil():
    try:
        conn = get_db()
        materiales = conn.execute('SELECT * FROM materiales').fetchall()
        conn.close()
        return render_template('albanil.html', materiales=materiales)
    except Exception as e:
        return f"<h1>❌ Error en Base de Datos (Albañil)</h1><p>{str(e)}</p>"

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cantidad = float(request.form['cantidad'])
    unidad = request.form['unidad']
    
    conn = get_db()
    conn.execute('INSERT INTO materiales (nombre, cantidad, unidad) VALUES (?, ?, ?)', (nombre, cantidad, unidad))
    conn.commit()
    conn.close()
    return redirect(url_for('panel_ingeniero'))

@app.route('/sacar', methods=['POST'])
def sacar():
    material_id = int(request.form['material_id'])
    cantidad_sacar = float(request.form['cantidad'])
    usuario = request.form['usuario']
    
    conn = get_db()
    material = conn.execute('SELECT * FROM materiales WHERE id = ?', (material_id,)).fetchone()
    
    if material and material['cantidad'] >= cantidad_sacar:
        nueva_cantidad = material['cantidad'] - cantidad_sacar
        conn.execute('UPDATE materiales SET cantidad = ? WHERE id = ?', (nueva_cantidad, material_id))
        conn.execute('INSERT INTO historial (material, cantidad, usuario) VALUES (?, ?, ?)', (material['nombre'], cantidad_sacar, usuario))
        conn.commit()
        conn.close()
        return "<h1>✅ Solicitud Registrada</h1><p>El material se ha descontado correctamente.</p><br><a href='/albanil_panel'>Volver al panel</a>"
    else:
        conn.close()
        return "<h1>❌ Error de Stock</h1><p>No hay suficiente material disponible o el material no existe.</p><br><a href='/albanil_panel'>Volver a intentar</a>"

if __name__ == '__main__':
    app.run(debug=True)
