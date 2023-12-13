from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from Db import db
from Db.models import users
from flask_login import LoginManager
from first import first

app = Flask(__name__)

# Секретный ключ, который обеспечит безопасность генерируемого JWT-токена
app = Flask(__name__)
app.secret_key = '123'

user_db='admin_kissing_both_site'
host_ip='127.0.0.1'
host_port=5432
database_name='kissing_both_site'
password='123'

app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

login_manager=LoginManager()
login_manager.login_view='first.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
	return users.query.get(int(user_id))

app.register_blueprint(first)