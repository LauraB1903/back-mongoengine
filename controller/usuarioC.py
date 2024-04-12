from flask import Flask, render_template, request, redirect, url_for, session, flash
from app import app, db
import json
import urllib.request
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

        recaptcha_response = request.form.get("g-recaptcha-response") 
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values ={
            'secret': '6LeCeLgpAAAAACkPykPj8_FgBnVOEc4GcZDZZklu',
            'response': recaptcha_response 
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
      
        user = Usuario.objects(usuario=usuario, contraseña=contraseña).first()

        if result["success"]:

            if user:
                session['usuario'] = usuario
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('agregar_producto'))
            else:
                flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.', 'error')
                return render_template('login.html')
        else:
            flash('No valido')


    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    
    return redirect(url_for('login'))