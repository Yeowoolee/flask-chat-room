# flask-chat-room

배포된 페이지: ~http://3.136.85.70:5000/~

> Goal

Flask, MongoDB Atlas, Socket.IO를 사용해 회원가입, 로그인, 채팅방을 선택해 실시간 채팅이 가능한 애플리케이션을 제작하고 AWS에 배포하는 것을 목표로 합니다.

### 1\. Flask에서 Socket.IO 사용하기

서버와 클라이언트 사이의 메시지 전달 과정과 내용은 이전의 채팅 앱 만들기와 같습니다.

채팅방을 선택해야 하기 때문에 join\_room, leave\_room를 사용했습니다.

```
from flask_socketio import SocketIO, send, emit, join_room, leave_room
```

클라이언트에서 채팅방에 접속하면 emit을 이용해 이벤트 이름, 메시지를 서버에 전송하도록 했습니다.

이벤트 이름 'join'  /  메시지 '{'username' : username, 'room' : room}'

```
function joinRoom(room){
        socket.emit('join', {'username' : username, 'room' : room});
        //메시지 출력 창 지우기
        document.querySelector('#display-message-section').innerHTML = ''
    }
```

마찬가지로 채팅방을 떠나면 emit을 이용해 이벤트 이름, 메시지를 서버에 전송하도록 했습니다.

이벤트 이름 'leave'  /  메시지 '{'username' : username, 'room' : room}'

```
  function leaveRoom(room){
        socket.emit('leave', {'username' : username, 'room' : room});
    }

```

'join'이 서버로 전달되었을 때

```
@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg':data['username'] + "님이 " + data['room'] + 
    "에 들어왔습니다."}, room=data['room'])
```

@socktio.on('join') : 'join'이 전달되었을 때 실행할 함수임을 알립니다.

매개변수인 'data'에는 전달된 메시지가 들어있습니다.

유저가 접속했다는 메시지를 클라이언트에게 전달하기 위해 send로 클라이언트에게 메시지를 전달했습니다. 

'leave'가 서버로 전달되었을 때

```
@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg':data['username'] + "님이 " + data['room'] + 
    "에서 나갔습니다."}, room=data['room'])

```

@socktio.on('leave') : 'leave'가 전달되었을 때 실행할 함수임을 알립니다.

매개변수인 'data'에는 전달된 메시지가 들어있습니다.

유저가 나갔다는 메시지를 클라이언트에게 전달하기 위해 send로 클라이언트에게 메시지를 전달했습니다. 

### 2\. Flask-WTF과 MongoDB Atlas 사용

Flask-WTF은 Flask의 Form기능을 지원하는 라이브러리입니다.

회원가입과 로그인 폼을 만들기 위해서 사용했습니다.

```
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
```

Form이 필요한 기능들을 모아둔 .py 파일을 따로 만들고 필요할 때 import해서 사용했습니다.

StringField, PasswordField, SubmitField 를 사용했는데 각각 문자열 input, 패스워드 input, submit 버튼과 같습니다.

label 아이디와 유효성 규칙을 설정 할 수 있습니다.

회원가입을 예시로 설명하겠습니다.

```
from wtform import *
@app.route('/regist', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
        
    return render_template("regist.html", form=reg_form)
```

정의된 form class사용을 위해 wtform파일을 불러왔습니다.

reg\_form 변수에 RegistForm()에 정의된 내용을 삽입합니다.

그리고 form이라는 변수로 reg\_form을 "regist.html"로 보냅니다.

이제 "regist.html"에서도 RegistForm()에 정의된 내용을 사용 할 수 있습니다. 

폼에 입력된 아이디와 비밀번호의 값을 가져와서 회원가입에 사용합니다.

우선 DB에 동일한 아이디가 있는지 체크합니다.

동일한 아이디가 없다면 비밀번호를 암호화 한 후 DB에 아이디와 함께 저장합니다.

```
{% macro displayField(fieldName, placeholderValue) %}

    <div>
        {{ fieldName(class_='form-control',
            placeholder=placeholderValue, **kwargs) }}

        <ul>
            {% for error in fieldName.errors %}
                <li>{{ error }}</li>
            {% endfor %}
        </ul>
    </div>
{% endmacro %}
```

로그인, 회원가입에 폼 구조가 동일하기 때문에 jinja macro기능을 사용해서 불필요한 코드의 사용을 줄였습니다.

```
{% from "form_Structure.html" import displayField %}

{% extends "login-layout.html" %}

{% block title %}회원가입{% endblock %}

{% block content %}
<form class="px-4 py-3" action="{{ url_for('index') }}", method="POST">
    <h1>시작하기</h1>
        
        {{ displayField(form.username, '아이디', autocomplete="off",
            autofocus=true)}}
        {{ displayField(form.password, '비밀번호')}}
        {{ displayField(form.confirm_pswd, '비밀번호 재입력')}}

        <div>
            {{ form.submit_button(class_="btn btn-primary") }}
        </div>

        {{ form.csrf_token }}

    </form>
    <div class="dropdown-divider"></div>
        <a class="dropdown-item" href="/">이미 가입을 하셨나요?</a>
</div>
{% endblock %}
```

{% from "form\_Structure.html" import displayField %} 으로 폼 구조에 대한 내용을 displayField로 불러옵니다.

그리고 담을 내용을 작성합니다.

displayField('필드이름', 'placeholder', 그 외 이벤트...)와 같은 순서로 입력합니다.

csrf\_token는 form의 보안을 위해 사용했습니다.

### 3\. AWS 배포

위에 설명한 부분 이외에는 이전 채팅 어플리케이션 만들기와 크게 다르지 않아서 바로 배포로 넘어가겠습니다.

AWS는 Heroku와는 다르게 터미널을 사용이 조금 더 많고 필요한 라이브러리를 일일히 설치해야 하는 번거로움이 있습니다. 하지만 자잘한 오류가 적고 Procfile을 사용하지 않아도 되기 때문에 테스트 환경에서 오류 없이 실행되었다면 AWS에 파일만 그대로 옮긴 후 라이브러리를 설치하고 Flask를 실행시키면 배포가 완료됩니다.

Flask의 AWS 배포에 관한 내용은 아래 게시글에 정리되어 있습니다.  
https://yeowool0217.tistory.com/620
