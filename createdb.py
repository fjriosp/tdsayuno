# -*- coding: utf-8 -*-
from hashlib import md5 
from model import db

db.create_all()
db.session.commit()

