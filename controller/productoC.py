from flask import Flask, render_template, request, redirect, url_for, session, flash
from app import app, db


class Productos(db.Document):
    codigo = db.StringField(required=True)
    nombre = db.StringField(required=True)
    precio = db.IntField(required=True)
    categoria = db.StringField(required=True)
    foto = db.StringField(required=True)

@app.route('/agregar_producto', methods=['GET', 'POST'])
#Recibimos los datos del formulario del name
def agregar_producto():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        foto = request.files['foto']

        # Verificar si el código del producto ya existe en la base de datos
        if Productos.objects(codigo=codigo).first():
            flash('Ya existe un producto con ese código', 'error')
            return redirect(url_for('agregar_producto'))

        # Si el código no existe se guarda en la base de datos
        producto = Productos(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            categoria=categoria,
            foto=foto.filename
        )
        producto.save() #Esta es la instruccion que guarda el producto

        flash('Producto agregado correctamente', 'success') #Flask  es para mostrar los mensajes desde el lado del cliente
        return redirect(url_for('agregar_producto'))

    else:
        productos = Productos.objects().all()
        return render_template('agregar_producto.html', productos=productos)
    
    

@app.route('/consultar_producto', methods=['GET'])
def consultar_producto():
    codigo = request.args.get('codigo')
    producto = Productos.objects(codigo=codigo).first()
    if producto:
        return render_template('producto_encontrado.html', producto=producto)
    else:
        flash(f'No se encontró el producto con el código: {codigo}', 'error')
    return redirect(url_for('producto_no_encontrado', codigo=codigo))


    
#Esta funcion es para que se muestre en un documento aparte si no encontró el producto   
@app.route('/producto_no_encontrado')    
def producto_no_encontrado():
    return render_template('producto_no_encontrado.html') 

#Esta funcion es para que se muestre en un documento aparte si encontró el producto   
@app.route('/producto_encontrado')    
def producto_encontrado():
    return render_template('producto_encontrado.html') 


   

@app.route('/editar_producto/<string:codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    producto = Productos.objects(codigo=codigo).first()
    if not producto:
        flash('El producto no existe', 'error')
        return redirect(url_for('agregar_producto'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        foto = request.files['foto'] if 'foto' in request.files else None

        producto.nombre = nombre
        producto.precio = precio
        producto.categoria = categoria
        if foto:
            producto.foto = foto.filename
        producto.save()

        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('agregar_producto'))

    else:
        return render_template('editar_producto.html', producto=producto)
    
    
from flask import abort

@app.route('/eliminar_producto/<string:codigo>', methods=['POST'])
def eliminar_producto(codigo):
    producto = Productos.objects(codigo=codigo).first()
    
    if producto:
        producto.delete()
        return redirect(url_for('agregar_producto'))
    else:
        abort(404, "El producto no existe")