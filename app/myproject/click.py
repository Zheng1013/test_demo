from myproject import db, login_manager, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Favorite(db.Model):
    __tablename__ = 'clickdata'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 添加其他字段，如时间戳、按钮ID等
    item_id = db.Column(db.Integer)
    # 添加其他字段，根据需要
    
    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id