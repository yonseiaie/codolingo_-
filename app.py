from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os, json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return {}
    
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/')
def homepage_start():
    return render_template('homepage_start.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = load_users()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')

        if not username or not password:
            flash('아이디와 비밀번호를 모두 입력해주세요.')
            return render_template('웹프로젝트회원가입.html')

        if username in users:
            flash('이미 존재하는 아이디입니다. 로그인해주세요.')
            return redirect('/login')

        users[username] = generate_password_hash(password)
        save_users(users)
        flash('회원가입 완료! 로그인 해주세요.')
        return redirect('/login')

    return render_template('웹프로젝트회원가입.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')

        if not username or not password:
            flash('아이디와 비밀번호를 모두 입력해주세요.')
            return render_template('웹프로젝트로그인.html')

        if username not in users or not check_password_hash(users[username], password):
            flash('아이디 또는 비밀번호가 올바르지 않습니다.')
            return render_template('웹프로젝트로그인.html')

        session['username'] = username
        return redirect('/start')

    return render_template('웹프로젝트로그인.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('로그아웃되었습니다.')
    return redirect('/')

@app.route('/start')
def start():
    if 'username' not in session:
        return redirect('/login')
    return render_template('homepage.html', username=session['username'])

@app.route('/concept/print')
def concept_print():
    if 'username' not in session:
        return redirect('/login')
    return render_template('print.html', username=session['username'])


@app.route('/concept/variable')
def concept_variable():
    if 'username' not in session:
        return redirect('/login')
    return render_template('variable.html', username=session['username'])

@app.route('/badge/1')
def badge1():
    return render_template('congratulation.html')

@app.route('/badge/2')
def badge2():
    return render_template('congratulation2.html')

@app.route('/sandbox')
def sandbox():
    if 'username' not in session:
        return redirect('/login')
    return render_template('sandbox.html', username=session['username'])

@app.route('/next_from_print')
def next_from_print():
    return redirect(url_for('badge1'))

if __name__ == '__main__':
    app.run(debug=True)
