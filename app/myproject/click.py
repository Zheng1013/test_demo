from myproject import db, login_manager, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class ClickEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 添加其他字段，如时间戳、按钮ID等
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    button_id = db.Column(db.Integer)
    # 添加其他字段，根据需要