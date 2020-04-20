from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistForm(FlaskForm):
    #회원가입

    username = StringField('username_label', 
            validators=[InputRequired(message="사용 할 수 없는 아이디입니다."),
            Length(min=4, max=25, message="아이디 길이는 4 ~ 25자로 제한됩니다.")])
    password = PasswordField('password_label',
            validators=[InputRequired(message="사용 할 수 없는 패스워드입니다."),
            Length(min=4, max=25, message="패스워드 길이는 4 ~ 25자로 제한됩니다.")])
    confirm_pswd = PasswordField('confirm_pswd_label',
            validators=[InputRequired(message="사용 할 수 없는 패스워드입니다."),
            EqualTo('password', message="패스워드가 일치하지 않습니다.")])
    submit_button = SubmitField('Create')