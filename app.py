from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Inicializar productos en la sesión si no existen
def init_session():
    if 'productos' not in session:
        session['productos'] = []



@app.route('/')
def index():
    init_session()
    return render_template('index.html', productos=session['productos'])


@app.route('/nuevo_producto')
def nuevo_producto():
    return render_template('nuevo_producto.html')

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    init_session()
    
    nuevo_id = request.form['id']
    
    
    if not nuevo_id.isdigit():
        flash("El ID debe ser un número entero.")
        # return render_template('nuevo_producto.html', error="El ID debe ser un número entero.")
        return redirect('/nuevo_producto')
    
    # Verificar si el ID ya existe
    for producto in session['productos']:
        if producto['id'] == nuevo_id:
            flash("El ID ya existe. Ingrese un ID único.")
            # return render_template('nuevo_producto.html', error="El ID ya existe. Ingrese un ID único.")
            return redirect('/nuevo_producto')
    
    producto = {
        'id': request.form['id'],
        'nombre': request.form['nombre'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }
    session['productos'].append(producto)
    session.modified = True
    return redirect('/')


@app.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    init_session()
    if request.method == 'POST':
        for producto in session['productos']:
            if int(producto['id']) == producto_id:
                producto['nombre'] = request.form['nombre']
                producto['cantidad'] = int(request.form['cantidad'])
                producto['precio'] = float(request.form['precio'])
                producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
                producto['categoria'] = request.form['categoria']
                session.modified = True
                break
        return redirect('/')
    return render_template('editar.html', producto_id=producto_id)

# eliminar producto
@app.route('/eliminar/<int:producto_id>')
def eliminar_producto(producto_id):
    init_session()
    session['productos'] = [
        prod for prod in session['productos'] 
        if not prod['id'].isdigit() or int(prod['id']) != producto_id
    ]
    session.modified = True
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
