from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length




class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=8, max=150)])
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=8, max=150)])
    submit = SubmitField('注册')
