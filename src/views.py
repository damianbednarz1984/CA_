from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from .models import Rooms


views = Blueprint("views", __name__)
mail = Mail()



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
	return render_template("user/user_dashboard.html", user=current_user)

# this route for handle changing user password from admin panel
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
