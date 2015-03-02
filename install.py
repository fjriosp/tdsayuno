# -*- coding: utf-8 -*-
from hashlib import md5 
from model import db,User,Version

db.create_all()

v = Version('0.1')
db.session.add(v)

u = User('admin', 'Administrador', 'fjriosp@gmail.com', md5('admin'+'patata').hexdigest(), 0)
db.session.add(u)

db.session.commit()

