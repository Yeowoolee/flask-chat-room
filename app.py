from flask import Flask, render_template
from wtform import *


app = Flask(__name__)
app.secret_key = 'mysecret'

@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistForm()
    if reg_form.validate_on_submit():
        #회원가입 폼의 모든 유효성검사가 pass 되면 실행
        
        return "아이디/패스워드가 조건에 맞습니다."
    return render_template("index.html", form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)