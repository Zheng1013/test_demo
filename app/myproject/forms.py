from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator
from wtforms import ValidationError

from myproject.models import User

class LoginForm(FlaskForm):
    email = StringField('電子郵件', validators=[DataRequired(), Email()])
    password = PasswordField('密碼',validators=[DataRequired()])
    submit = SubmitField('登入')

class RegistrationForm(FlaskForm):
    email = StringField('電子郵件', validators=[DataRequired(), Email()])
    username = StringField('使用者', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired(), EqualTo('password_confirm', message='密碼需要吻合')])
    password_confirm = PasswordField('確認密碼', validators=[DataRequired()])
    submit = SubmitField('註冊')

    def validate_email(self, field):
        """檢查Email"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('電子郵件已經被註冊過了')

    def validate_username(self, field):
        """檢查username"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('使用者名稱已經存在')
