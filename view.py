# -*- coding: utf-8 -*-
import time
from functools import wraps
from uuid import uuid4
from hashlib import md5 
from flask import Flask, request, redirect, url_for, render_template, make_response

app = Flask('tdsayuno',static_url_path='')

from model import db,User,Food,Drink

# Devuelve el usuario que está autenticado
def getUserBySession():
  session = request.cookies.get('session')
  if not session:
    return None
  if session:
    u = User.query.filter_by(session=session).first()
  return u

def auth(f,admin=False):
  @wraps(f)
  def auth_f(*args, **kwargs):
    u = getUserBySession()
    if not u:
      return redirect(url_for('index'))
    if admin and not u.isAdmin:
      return redirect(url_for('index'))
    kwargs['user'] = u
    return f(*args, **kwargs)
  return auth_f

@app.route('/')
def index():
  u = getUserBySession()
  if not u:
    return render_template('login.html')

  return render_template('index.html',u=u)

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return redirect(url_for('index'))

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
@auth  
def logout(user):
  user.session = None
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/perfil', methods=['GET','POST'])
@auth  
def perfil(user):
  if request.method == 'GET':
    return render_template('perfil.html',u=user)

  name = request.form['name']
  passwd = request.form['passwd']
  mail = request.form['mail']
  
  user.name = name
  user.passwd = passwd
  user.mail = mail
  db.session.commit()

  return redirect(url_for('index'))

@app.route('/comida')
@auth  
def comida(user):
  id = request.args.get('id')

  edit = None
  if id:
    edit = Food.query.filter_by(id=id).first()

  food_list = Food.query.all()

  return render_template('comida.html',productos=food_list,e=edit,u=user)

@app.route('/saveComida', methods=['POST'])
@auth  
def saveComida(user):
  id = None
  if 'id' in request.form:
    id = request.form['id']
  name = request.form['name']
  price = request.form['price']

  if id:
    f = Food.query.filter_by(id=id).first()
    f.name = name
    f.price = price
  else:
    f = Food(name,price)
    db.session.add(f)

  db.session.commit()

  return redirect(url_for('comida'))

@app.route('/deleteComida')
@auth  
def deleteComida(user):
  id = int(request.args.get('id'))

  f = Food.query.filter_by(id=id).first()
  db.session.delete(f)
  db.session.commit()

  return redirect(url_for('comida'))

@app.route('/bebida')
@auth  
def bebida(user):
  id = request.args.get('id')

  edit = None
  if id:
    edit = Drink.query.filter_by(id=id).first()

  drink_list = Drink.query.all()

  return render_template('bebida.html',productos=drink_list,e=edit,u=user)

@app.route('/saveBebida', methods=['POST'])
@auth  
def saveBebida(user):
  id = None
  if 'id' in request.form:
    id = request.form['id']
  name = request.form['name']
  price = request.form['price']

  if id:
    f = Drink.query.filter_by(id=id).first()
    f.name = name
    f.price = price
  else:
    f = Drink(name,price)
    db.session.add(f)

  db.session.commit()

  return redirect(url_for('bebida'))

@app.route('/deleteBebida')
@auth  
def deleteBebida(user):
  id = int(request.args.get('id'))

  f = Drink.query.filter_by(id=id).first()
  db.session.delete(f)
  db.session.commit()

  return redirect(url_for('bebida'))

def start(debug=False):
  app.run(host='0.0.0.0',debug=debug)

if __name__ == '__main__':
  start(debug=True)
