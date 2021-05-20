from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, fname=first_name, lname=last_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account has been created successfully. Please login to continue...', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)


@auth.route("/reset_password")
def reset_password():
    return render_template("forgot_pass.html", user=current_user)


@auth.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    
    if request.method == "GET":
        return render_template("user/change_password.html", user=current_user)
    
    if request.method == "POST":
        old_pass = request.form.get("old_pass")
        new_pass = request.form.get("new_pass")
        re_pass = request.form.get("re_pass")
 
        if new_pass == re_pass:
            
            if check_password_hash(current_user.password, old_pass):
                gen_hash_pass = generate_password_hash(new_pass, method="sha256")
                User.query.filter_by(id=current_user.id).update(dict(password=gen_hash_pass))
          
                db.session.commit()
                flash("Your password has been changed successfully", category='success')
                return redirect(url_for('auth.change_password'))
            
            else:
                flash("Old password doesn't match!", category='error')
                return redirect(url_for('auth.change_password'))
       
        else:
            flash("Couldn't match New password and Confirm password!", category='error')
            return redirect(url_for('auth.change_password'))
