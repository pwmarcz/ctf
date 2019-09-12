from flask import Flask, render_template, request, redirect
import time

app = Flask(__name__)


@app.route('/forum/')
def forum():
    username = request.cookies.get('forum_user')
    if not username:
        return redirect('/forum/login/')

    return render_template('forum.html', username=username)


@app.route('/forum/logout/')
def logout():
    resp = redirect('/forum/login/')
    resp.set_cookie('forum_user', '')
    return resp


@app.route('/forum/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print('login POST:', username, password)
        if username == 'guest' and password == 'guest':
            resp = redirect('/forum/')
            resp.set_cookie('forum_user', username)
            return resp
        return render_template('login.html', incorrect_login=True)

    return render_template('login.html')
