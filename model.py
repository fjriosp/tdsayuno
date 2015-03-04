from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import time

app = Flask('tdsayuno')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tdsayuno.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.String)
  name = db.Column(db.String)
  mail = db.Column(db.String)
  passwd = db.Column(db.String)
  session = db.Column(db.String)
  seed = db.Column(db.Integer)
  karma = db.Column(db.Integer)
  food = db.Column(db.Integer)
  drink = db.Column(db.Integer)
  pref_food = db.Column(db.Integer)
  pref_drink = db.Column(db.Integer)

  def __init__(self, user, name, mail, passwd, karma):
    self.user = user
    self.name = name
    self.mail = mail
    self.passwd = passwd
    self.session = None
    self.seed = int(time.time() * 1000)
    self.karma = karma
    self.food = None
    self.drink = None
    self.pref_food = None
    self.pref_drink = None

  def isAdmin(self):
    return self.user=='admin'

  def __str__(self):
    return 'User(%d,"%s","%s","%s","%s",%d,%d,%d,%d,%d,%d)' % (self.id,self.user,self.name,self.mail,self.session,self.seed,self.karma,self.food,self.drink,self.pref_food,self.pref_drink)

class Version(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  version = db.Column(db.String)

  def __init__(self, version):
    self.version = version

  def __str__(self):
    return 'Version(%d,"%s")' % (self.id,self.version)

class Drink(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  price = db.Column(db.Float)

  def __init__(self, name, price):
    self.name = name
    self.price = price

  def __str__(self):
    return 'Drink(%d,"%s",%f)' % (self.id,self.name,self.price)

class Food(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  price = db.Column(db.Float)

  def __init__(self, name, price):
    self.name = name
    self.price = price

  def __str__(self):
    return 'Food(%d,"%s",%f)' % (self.id,self.name,self.price)

