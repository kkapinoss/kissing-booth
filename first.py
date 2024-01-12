from flask import Blueprint, render_template, request, redirect, session
from Db import db
from Db.models import users, anc
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

first = Blueprint('first', __name__)


@first.route("/")
def start():
	return redirect("/first", code=302)


# @first.route("/first/check")
# def star():
# 	my_users = users.query.all()
# 	print(my_users)
# 	return "result in cosole!"


# @first.route("/first")
# def base():
# 	return render_template("base.html")


@first.route('/first')
def main():
	# if current_user.is_authenticated:
	# 	username = current_user.username
	# else:
	# 	username = "Аноним"
	return render_template('base.html')


@first.route('/glav')
def mains():
	if current_user.is_authenticated:
		username = current_user.username
	else:
		username = "Аноним"
	return render_template('glav.html', username=username)



# @first.route ("/first")
# def main():
#     username=session.get("username")
#     if username =='':
#         visibleUser='Anon'
#     else:
#         visibleUser=username
#     return render_template('base.html',username=visibleUser)

# АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ
@first.route('/first/login', methods=['GET', 'POST'])
def login():
	error=''
	if request.method=='GET':
		return render_template('login.html')

	username_form=request.form.get('username')
	password_form=request.form.get('password')

	if username_form=='' or password_form=='':
		error="Let's try again"
		return render_template('login.html', error=error)

	my_user=users.query.filter_by(username=username_form).first()

	if my_user is not None:
		if check_password_hash(my_user.password, password_form):
			login_user(my_user, remember=False)
			return redirect('/glav')
		else:
			error='Incorrect password'
			return render_template('login.html', error=error) 
	else:
		error='User does not exist'
		return render_template('login.html', error=error)

# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
@first.route('/first/regist', methods=['GET', 'POST'])
def regist():
	errors=''

	if request.method=='GET':
		return render_template('regist.html')

	username_form=request.form.get('username')
	password_form=request.form.get('password')

	if username_form == '':
		errors="Let's try again" 
		return render_template('regist.html', errors=errors)

	if len(password_form)<5:
		errors='Password is less than 5'
		return render_template('regist.html', errors=errors)

	isUserExists=users.query.filter_by(username=username_form).first()

	if isUserExists is not None:
		errors='Already exists'
		return render_template('regist.html', errors=errors)

	hashedPswd=generate_password_hash(password_form, method='pbkdf2')
	newUser=users(username=username_form, password=hashedPswd)

	db.session.add(newUser)
	db.session.commit()

	return redirect('/first/login')


#Выход из аккаунта
@first.route('/first/logout')
@login_required
def logout():
    logout_user()
    return redirect('/first')


@first.route('/first/delete', methods=['POST'])
@login_required
def delete():
    user_id = current_user.id
    user = users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect('/login')


@first.route('/stran', methods=['POST', 'GET'])
@login_required
def page():
    if request.method=='GET':
        return render_template('stran.html')

    name = request.form.get('urname')
    gender = request.form.get('urmale')
    search_gender = request.form.get('urfindmale')
    about = request.form.get('urinfo')
    photo = request.form.get('urphoto')
    user_id = current_user.id

    if request.form.get('urage') == '':
        age=request.form.get('urage')
    else:
        age = int(request.form.get('urage'))
        if age<18 or age>100:
            errors='Некорректный возраст'
            return render_template('stran.html',errors=errors,urname=name,urmale=gender,urfindmale=search_gender,urinfo=about,urphoto=photo)
    
    if name=='' or gender=='' or search_gender=='':
        errors='Пожалуйста, заполните все поля'
        return render_template('stran.html',errors=errors,urname=name,urage=age,urmale=gender,urfindmale=search_gender,urinfo=about,urphoto=photo)
    

    new_form = anc(user_id=user_id, name=name, age=age, gender=gender, search_gender=search_gender, about=about, photo=photo)
    db.session.add(new_form)
    db.session.commit()
    return redirect('/glav')


@first.route('/first/page_change', methods=['POST', 'GET'])
@login_required
def page_change():
    user_id = current_user.id
    existing_form = anc.query.filter_by(user_id=user_id).first()
    
    if request.method == 'GET':
        return render_template('page_change.html', form=existing_form)

    name = request.form.get('urname')
    gender = request.form.get('urmale')
    search_gender = request.form.get('urfindmale')
    about = request.form.get('urinfo')
    photo = request.form.get('urphoto')
    
    if request.form.get('urage') == '':
        age = None
    else:
        age = int(request.form.get('urage'))
        if age < 18 or age > 100:
            errors = 'Некорректный возраст'
            return render_template('page_change.html', errors=errors, form=existing_form)
    
    if name == '' or gender == '' or search_gender == '':
        errors = 'Пожалуйста, заполните все поля'
        return render_template('page_change.html', errors=errors, form=existing_form)

    existing_form.name = name
    existing_form.age = age
    existing_form.gender = gender
    existing_form.search_gender = search_gender
    existing_form.about = about
    existing_form.photo = photo

    db.session.commit()
    return redirect('/glav')

#Поиск
@first.route('/search', methods=['POST'])
@login_required
def search():
    findname = request.form.get('findname')
    findage = request.form.get('findage')
    find_gender = anc.query.filter_by(user_id=current_user.id).first().search_gender

    if findname and findage:
        profiles = anc.query.filter(anc.name.ilike(f"%{findname}%"), anc.age == findage, anc.gender == find_gender).limit(3)
    elif findname:
        profiles = anc.query.filter(anc.name.ilike(f"%{findname}%"), anc.gender == find_gender).limit(3)
    elif findage:
        profiles = anc.query.filter(anc.age == findage, anc.gender == find_gender).limit(3)
    else:
        profiles = anc.query.filter(anc.gender == find_gender).limit(3)

    if profiles.count() == 0:
        return render_template('error.html')

    return render_template('glav.html', profiles=profiles, username=current_user.username, findname=findname,findage=findage)



@first.route('/loadmore', methods=['POST'])
@login_required
def load_more_profiles():
    last_displayed_profile_id = request.form.get('last_displayed_profile_id')
    findname = request.form.get('findname')
    findage = request.form.get('findage')

    find_gender = anc.query.filter_by(user_id=current_user.id).first().search_gender

    if findname and findage:
        next_profiles = anc.query.filter(anc.id > last_displayed_profile_id,
                                          anc.name.ilike(f"%{findname}%"),
                                          anc.age == findage,
                                          anc.gender == find_gender).limit(3).all()
    elif findname:
        next_profiles = anc.query.filter(anc.id > last_displayed_profile_id,
                                          anc.name.ilike(f"%{findname}%"),
                                          anc.gender == find_gender).limit(3).all()
    elif findage:
        next_profiles = anc.query.filter(anc.id > last_displayed_profile_id,
                                          anc.age == findage,
                                          anc.gender == find_gender).limit(3).all()
    else:
        next_profiles = anc.query.filter(anc.id > last_displayed_profile_id,
                                          anc.gender == find_gender).limit(3).all()

    return render_template('glav.html', profiles=next_profiles, username=current_user.username,findname=findname,findage=findage)