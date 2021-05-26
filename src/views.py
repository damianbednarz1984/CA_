from flask import Blueprint, render_template,redirect, request, flash, jsonify,url_for
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from .models import Rooms, User
from . import db
import os
import shutil
from datetime import date, timedelta
import datetime



views = Blueprint("views", __name__)
mail = Mail()

def default_avatar():
	if not os.path.exists("src/static/img/user_avatars/default_user_img.png"):
		shutil.copy("src/static/img/default_user_img.png", "src/static/img/user_avatars/default_user_img.png")

def check_in_date(chk_in):
    chk_in_y = int(chk_in.split('-')[0])
    chk_in_m = int(chk_in.split('-')[1])
    chk_in_d = int(chk_in.split('-')[2])
    chk_in = date(chk_in_y, chk_in_m, chk_in_d)
    return chk_in
def check_out_date(chk_out):
    chk_out_y = int(chk_out.split('-')[0])
    chk_out_m = int(chk_out.split('-')[1])
    chk_out_d = int(chk_out.split('-')[2])
    chk_out = date(chk_out_y, chk_out_m, chk_out_d)
    return chk_out
def daterange(chkin, chkout):
    for n in range(int ((chkout - chkin).days)+1):
        yield chkin + timedelta(n)


@views.route("/", methods=["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
def home():
	if request.method == "GET":
		return render_template("home.html", user=current_user)
	if request.method == "POST":
		full_name = request.form.get("full_name")
		email = request.form.get("email")
		subject = request.form.get("subject")
		msg = request.form.get("message")
		mail_template = Message("A new contact submission!", sender='damianbednarz1984@gmail.com', recipients=['damianbednarz1984@gmail.com'])
		mail_template.body = f"Name : {full_name}\nFrom : {email}\nSubject : {subject}\n\n{msg}"
		mail.send(mail_template)
		return jsonify("Your email has been sent successfully, We'll response as soon as posible... Thank you")

	

@views.route("/rooms")
def rooms():
	rooms = Rooms.query.all()
	return render_template("rooms.html", user=current_user, room=rooms)	
	

@views.route("/room_book", methods=["GET", "POST"])	
def room_book():
	room_id = request.args.get("room_id")
	room_data = Rooms.query.filter_by(id=room_id).first()
	return render_template("room_book.html", user=current_user, room_data=room_data)




@views.route("/contact", methods=["GET", "POST"])
def contact():
	if request.method == "GET":
		return render_template("contact.html", user=current_user)
	if request.method == "POST":
		fname = request.form.get("fname")
		lname = request.form.get("lname")
		email = request.form.get("email")
		subject = request.form.get("subject")
		msg = request.form.get("message")

		mail_template = Message("A new contact submission!", sender='damianbednarz1984@gmail.com', recipients=['damianbednarz1984@gmail.com'])
		mail_template.body = f"Name : {fname} {lname}\nFrom : {email}\nSubject : {subject}\n\n{msg}"
		mail.send(mail_template)
		return jsonify("Your email has been sent successfully, We'll response as soon as posible... Thank you")

@views.route("/user_dashboard")
@login_required
def user_dashboard():
	default_avatar()
	return render_template("user/user_dashboard.html", user=current_user)

# this route for handle changing user password 
@views.route("/change_user_pass", methods=["POST"])
@login_required
def change_user_pass():
	
	pass_user_id = request.form.get("pass_user_id")
	old_pass = request.form.get("old_pass")
	new_pass = request.form.get("new_pass")
	
	fetch_old_pass = User.query.filter_by(id=pass_user_id).first()
	
	if check_password_hash(fetch_old_pass.password, old_pass):
		gen_new_hash = generate_password_hash(new_pass, method="sha256")
		User.query.filter_by(id=pass_user_id).update(dict(password=gen_new_hash))
		db.session.commit()
		flash("Password has changed successfully", category="success")
		return redirect(url_for("views.user_modify", user_id=pass_user_id))
	else:
		flash("Old password doesn't match!", category="error")
		return redirect(url_for("views.user_modify", user_id=pass_user_id))

@views.route("/user_personal_info", methods=["GET", "POST"])
@login_required
def user_personal_info():
	fname = request.form.get("fname")
	lname = request.form.get("lname")
	email = request.form.get("email")
	phone = request.form.get("phone")
	birth = request.form.get("birth")
	country = request.form.get("country")
	gender = request.form.get("gender")
	city = request.form.get("city")
	zip_code = request.form.get("zip_code")
	address = request.form.get("address")
	user_id = request.form.get("user_id")
	modify_user = User.query.filter_by(id=user_id).update(dict(fname=fname, lname=lname, email=email, phone=phone, date_of_birth=birth, country=country, gender=gender, city=city, zip_code=zip_code, address=address))
	db.session.commit()
	default_avatar()
	return redirect(url_for('views.user_dashboard'))

	