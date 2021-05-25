from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail_user
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import os
import random
import string


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

@auth.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("forgot_pass.html", user=current_user)

@auth.route("/password_reset_confirmation_url/<string:hashCode>")
def password_reset_confirmation_url(hashCode):
 
    fetch_hash = User.query.filter_by(hashCode=hashCode).first()
    if fetch_hash:
       
        return render_template("set_new_pass.html", user_id=fetch_hash.id, user=current_user)
    else:
        flash("Password reset link has been expired", category="error")
        return redirect(url_for("auth.login"))

@auth.route("/set_new_pass", methods=["GET", "POST"])
def set_new_pass():
    if request.method == "POST":
        password = request.form.get("password")
        user_id = request.form.get("user_id")
        User.query.filter_by(id=user_id).update(dict(password=generate_password_hash(password, method="sha256"), hashCode=0))
        db.session.commit()
        # if password has changed then redirect to login page
        flash("Your password has been changed successfully", category="success")
        return redirect(url_for('auth.login'))


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

            
@auth.route("/user_account_delete", methods=["POST"])
@login_required
def user_account_delete():
    password = request.form.get("password")
    if check_password_hash(current_user.password, password):
        fetch_user = User.query.filter_by(id=current_user.id).first()
        os.remove(f"src/static/img/user_avatars/{fetch_user.avatar}")
        db.session.delete(fetch_user)
        db.session.commit()
        flash("Account has been deleted permanently", category="success")
        return redirect(url_for('auth.login'))
    else:
        flash("Invalid password! please try again...", category="error")
        return redirect(url_for('views.user_dashboard'))
