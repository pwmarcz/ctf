from flask import Flask, render_template, request

app = Flask(__name__)

PASSWORDS = {'Harry Smith': 'xZ6YUr4solKIELMI9GBl',
             'Oliver Jones': 'avHtDfIa50Luxw5vk52t',
             'Sally Young': 'ZiL2cvLxiQHJYDYeXeYt',
             'Maia Booker': 'gtqrqb2VpDa9nRIwJF43',
             'Lukasz Kowalski': 'RgAhM2bo6hpQzgLqNp6F'}

@app.route('/name/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').encode('ascii').decode()
        password = request.form.get('password').encode('ascii').decode()
        if PASSWORDS.get(username) == password:
            return render_template('login.html', login_correct=True)
        return render_template('login.html', login_incorrect=True)
    return render_template('login.html')
