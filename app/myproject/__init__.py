import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# flask_login
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']= 'acretkeyinthisproject'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:zxas014208@localhost:3306/data"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'