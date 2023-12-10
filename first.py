from flask import Blueprint, render_template, url_for, redirect

first = Blueprint('first', __name__)

@first.route("/")
def start():
	return redirect("/first", code=302)


@first.route("/first")
def base():
	return render_template("base.html")