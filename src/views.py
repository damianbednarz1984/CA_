from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_mail import Mail, Message



views = Blueprint("views", __name__)
mail = Mail()

@views.route("/", methods=["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
def home():
	if request.method == "GET":
		return render_template("home.html", user=current_user)
	

	


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

# future function for user dashboard 
# @views.route("/user_dashboard") 
# @login_required
# def user_dashboard():
