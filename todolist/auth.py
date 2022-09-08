from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('views.task_list'))

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.task_list'))
            else:
                flash("Incorrect password, try again", category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if current_user.is_authenticated:
        return redirect(url_for('views.task_list'))

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.", category='error')

        elif len(first_name) < 2:
            flash("First name must be greater than 1 characters.", category='error')

        elif password1 != password2:
            flash("Passwords don\'t match.", category='error')

        elif len(password1) < 4:
            flash("Password must be at least 4 characters long.", category='error')

        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), first_name=first_name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('views.task_list'))

    return render_template("sign_up.html", user=current_user)






