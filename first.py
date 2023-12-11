from flask import Blueprint, render_template, request, make_response, redirect, session
from Db import db
from Db.models import users, anceta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user

first = Blueprint('first', __name__)

@first.route("/")
def start():
	return redirect("/first", code=302)


# @first.route("/first")
# def base():
# 	return render_template("base.html")


# @first.route('/first')
# def main():
# 	if current_user.is_authenticated:
# 		username = current_user.username
# 	else:
# 		username = "Аноним"
# 	return render_template('base.html', username=username)


@first.route ("/first")
def main():
    username=session.get("username")
    if username =='':
        visibleUser='Anon'
    else:
        visibleUser=username
    return render_template('base.html',username=visibleUser)


# @first.route('/first/login', methods=['GET', 'POST'])
# def login():
# 	error=''
# 	if request.method=='GET':
# 		return render_template('login.html')

# 	username_form=request.form.get('username')
# 	password_form=request.form.get('password')

# 	if username_form=='' or password_form=='':
# 		error='не заполнены поля'
# 		return render_template('login.html', error=error)

# 	my_user=users.query.filter_by(username=username_form).first()

# 	if my_user is not None:
# 		if check_password_hash(my_user.password, password_form):
# 			login_user(my_user, remember=False)
# 			return redirect('/first/articles')
# 		else:
# 			error='неверный пароль'
# 			return render_template('login.html', error=error) 
# 	else:
# 		error='такого пользователя не существует'
# 		return render_template('login.html', error=error)


@first.route('/first/regist', methods=['GET', 'POST'])
def regist():
	# return render_template('regist.html')
	errors=''

	if request.method=='GET':
		return render_template('regist.html')

	username_form=request.form.get('username')
	password_form=request.form.get('password')

	if username_form == '':
		errors='Пустое имя'
		return render_template('regist.html', errors=errors)

	if len(password_form)<5:
		errors='Пароль меньше 5'
		return render_template('regist.html', errors=errors)

	isUserExists=users.query.filter_by(username=username_form).first()

	if isUserExists is not None:
		errors='уже существует'
		return render_template('regist.html', errors=errors)

	hashedPswd=generate_password_hash(password_form, method='pbkdf2')
	newUser=users(username=username_form, password=hashedPswd)

	db.session.add(newUser)
	db.session.commit()

	return redirect('/first/login')