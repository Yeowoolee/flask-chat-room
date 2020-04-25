from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, session, flash

from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_pymongo import PyMongo
#Flask-PyMongo==2.3.0
from flask_bcrypt import Bcrypt
#flask-bcrypt==0.7.1
from wtform import *


app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_URI'] = "mongodb+srv://jinho0217:test@cluster0-klwld.gcp.mongodb.net/Flask_Chat_Room?retryWrites=true&w=majority"

socketio = SocketIO(app)
ROOMS = ['lobby', 'games', 'news']

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

        #회원가입 성공시 로그인 창으로
        flash('회원가입 성공!', 'success')
        return redirect(url_for('login'))
        
    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        msg = '등록되지 않은 '
        #등록 아이디 체크
        existing_user = myuser.find_one({'username' : username})
        if existing_user:
            pw_check = bcrypt.check_password_hash(existing_user['password'], password)    
            if pw_check:
                session['username'] = username
                return f"로그인 성공! 환영합니다. {session['username']} 님"
            else:
                msg += '패스워드 입니다.'
                return msg
        else:
            msg += '아이디 입니다.'
            return msg
    return render_template("login.html", form=login_form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('login'))

@app.route("/chat", methods=["GET", "POST"])
def chat():
    # if 'username' in session:
    #     return "chat 접속 성공"
    # else:
    #     flash('로그인이 필요한 페이지입니다.', 'danger')
    #     return redirect(url_for('login'))
    return render_template("chat.html", username=session['username'],
        rooms=ROOMS)


@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'],'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])
    
@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg':data['username'] + "님이 " + data['room'] + 
    "에 들어왔습니다."}, room=data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg':data['username'] + "님이 " + data['room'] + 
    "에서 나갔습니다."}, room=data['room'])



if __name__ == "__main__":
    socketio.run(app, debug=True)