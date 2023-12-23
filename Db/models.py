# Импортируем переменную db из файла __init__.py
from . import db
from flask_login import UserMixin

# Описваем схему наше БД в виде объектов
# Таким образом, сохдание таблиц возьмет на себя 
# SQLAlchemy - система ORM.

class users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.String(102), nullable=False)

	def __repr__(self):
		return f'id:{self.id}, username:{self.username}'

class anceta(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	name = db.Column(db.String(50), nullable=False)
	age = db.Column(db.Text, nullable=False)
	sex = db.Column(db.Boolean)
	about_me = db.Column(db.Text, nullable=False)
	likes = db.Column(db.Integer)

	def __repr__(self):
		return f'name:{self.name}, age:{self.age}, about_me:{self.about_me}'
	
class anc(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	name = db.Column(db.String(50), nullable=False)
	age = db.Column(db.Integer, nullable=False, default=0)
	gender = db.Column(db.String(10), nullable=False)
	search_gender = db.Column(db.String(10), nullable=False)
	about = db.Column(db.String(200))
	photo = db.Column(db.String(500))

	def repr(self):
		return f"Form('{self.user_id}', '{self.name}', '{self.age}', '{self.gender}', '{self.search_gender}')"