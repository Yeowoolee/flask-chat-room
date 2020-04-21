from flask import Flask, render_template
from flask_pymongo import PyMongo
#Flask-PyMongo==2.3.0
from flask_bcrypt import Bcrypt
#flask-bcrypt==0.7.1
from wtform import *


app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_URI'] = ""
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

myuser = mongo.db.users #유저 데이터베이스

@app.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistForm()
    if reg_form.validate_on_submit():
        #회원가입 폼의 모든 유효성검사가 pass 되면 실행
        username = reg_form.username.data
        password = reg_form.password.data

        #중복 아이디 체크
        existing_user = myuser.find_one({'username' : username})
        if existing_user:
            return "같은 아이디가 존재합니다."
        hashpass = bcrypt.generate_password_hash(password) #패스워드 암호화
        db_data = {'username':username, 'password':hashpass}
        myuser.insert_one(db_data)
        return "추가완료"

    return render_template("index.html", form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)