from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
DB_NAME = "database.db"
# this is the root of directory for all uploading images
UPLOAD_FOLDER = "src/static/img/"

mail_smtp = ""
mail_user = ""
mail_pass = ""
mail_port = 587
mail_subject = "TEST" # put here subject for email
mail_response = "Thanks for your email" 

chk_error_res = "Sorry this isn't available"
# all configurations
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjahkjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAIL_SERVER'] = mail_smtp
    app.config['MAIL_USERNAME'] = mail_user
    app.config['MAIL_PASSWORD'] = mail_pass
    app.config['MAIL_PORT'] = mail_port
    app.config['MAIL_USE_TLS'] = True
    app.config['DEFAULT_MAIL_SENDER'] = mail_user


    
    db.init_app(app)

    mail = Mail()
    mail.init_app(app)

    # making blueprint of these files
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# create database.db file if not exist in directory
def create_database(app):
    if not path.exists('src/' + DB_NAME):
        db.create_all(app=app)
        print('Database has been created successfully')