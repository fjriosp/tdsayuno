# -*- coding: utf-8 -*-
import time
from uuid import uuid4
from hashlib import md5 
from flask import Flask, request, redirect, url_for, render_template, make_response

app = Flask('tdsayuno',static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tdsayuno.db'

from model import db,User

# Devuelve el usuario que está autenticado
def getUserBySession():
  session = request.cookies.get('session')
  
  if not session:
    return None

  if session:
    u = User.query.filter_by(session=session).first()

  return u
  

@app.route('/')
def index():
  u = getUserBySession()
  if not u:
    return render_template('login.html')

  return render_template('index.html',user=u)

@app.route('/login', methods=['POST'])
def login():
  user = request.form['user']
  passwd = request.form['passwd']
  seed = int(request.form['seed'])

  print 'Intento de login del usuario "%s".' % (user)
  print user
  print passwd
  print seed

  # Compruebo que el usuario existe
  u = User.query.filter_by(user=user).first()
  if not u:
    print 'Usuario "%s" no encontrado.' % (user)
    return render_template('login.html',error='Login error')

  # Test de la marca de tiempo
  maxseed = int(time.time() * 1000) + 60000
  if u.seed >= seed or seed >= maxseed:
    print '¡¡Timestamp incorrecto!!'
    print u.seed
    print seed
    print maxseed
    return render_template('login.html',error='Login error')

  # Validación de contraseña
  checkpasswd = md5(u.passwd + str(seed)).hexdigest()
  if passwd != checkpasswd:
    print 'Contraseña errónea.'
    return render_template('login.html',error='Login error')
  
  # Genero un id de sessión
  session = str(uuid4())

  # Actualizo el usuario en base de datos
  u.session = session
  u.seed = seed
  db.session.commit()

  resp = make_response(redirect(url_for('index')))
  resp.set_cookie('session', u.session)
  return resp
  
@app.route('/logout')
def logout():
  u = getUserBySession()
  if not u:
    return redirect(url_for('index'))

  u.session = None
  db.session.commit()

  return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
