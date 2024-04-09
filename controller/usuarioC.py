from flask import Flask, render_template, request, redirect, url_for, session, flash
from app import app, db
# from mongoengine import Document,StringField

class Usuario(db.Document):
    usuario = db.StringField(required=True)
    contraseña = db.StringField(required=True)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
      
        user = Usuario.objects(usuario=usuario, contraseña=contraseña).first()

        if user:
            session['usuario'] = usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('agregarProducto'))
        else:
            flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    
    return redirect(url_for('login'))