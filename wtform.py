from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo
#wtform 에서 제공하는 폼을 사용.
#유효성 검사 제공.
   

class RegistForm(FlaskForm):
    #회원가입

    username = StringField('username_label', 
            validators=[InputRequired(message="아이디를 입력하세요."),
            Length(min=4, max=25, message="아이디 길이는 4 ~ 25자로 제한됩니다.")])
    password = PasswordField('password_label',
            validators=[InputRequired(message="패스워드를 입력하세요."),
            Length(min=4, max=25, message="패스워드 길이는 4 ~ 25자로 제한됩니다.")])
    confirm_pswd = PasswordField('confirm_pswd_label',
            validators=[InputRequired(message="사용 할 수 없는 패스워드입니다."),
            EqualTo('password', message="패스워드가 일치하지 않습니다.")])
    submit_button = SubmitField('회원가입')

class LoginForm(FlaskForm):
    #로그인
    username = StringField('username_label', 
            validators=[InputRequired(message="아이디를 입력하세요.")])
    password = PasswordField('password_label', 
            validators=[InputRequired(message="패스워드를 입력하세요.")])
    submit_button = SubmitField('로그인')