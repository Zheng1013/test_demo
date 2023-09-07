from myproject import db, login_manager, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class ClickEvent(db.Model):
    click_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer)

    def __init__(self, id, item_id):
        """初始化"""
        self.email = id
        self.username = item_id
