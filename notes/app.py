from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/notes/'
app.secret_key = 'notes!'

# https://werkzeug.palletsprojects.com/en/0.15.x/middleware/proxy_fix/#module-werkzeug.middleware.proxy_fix
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/notes/')
def notes():
    username = session.get('notes_user')
    if not username:
        return redirect(url_for('login'))

    return render_template('notes.html', username=username)


@app.route('/notes/logout/')
def logout():
    del session['notes_user']
    return redirect(url_for('login'))


@app.route('/notes/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print('login POST:', username, password)
        if username == 'guest' and password == 'guest':
            session['notes_user'] = username
            return redirect(url_for('notes'))
        return render_template('login.html', incorrect_login=True)

    return render_template('login.html')


@app.route('/notes/user/')
@app.route('/notes/user/<username>/')
def list(username=None):
    if not username:
        username = session.get('notes_user')
        return redirect(url_for('list', username=username))

    result = []
    for uuid, note in NOTES.items():
        if username == note['user']:
            result.append({'uuid': uuid, 'topic': note['topic']})
    return jsonify(result)


@app.route('/notes/<uuid>/')
def note(uuid):
    if uuid not in NOTES:
        return Response('Not found', status=404)
    note = NOTES[uuid]
    result = {'uuid': uuid, **note}
    return jsonify(result)


# IDs generated with: [str(uuid.uuid4()) for i in range(10)]
NOTES = {
    '3609d7af-0e42-4c49-84fc-b5c157760db2': {
        'user': 'guest',
        'topic': 'Welcome to my app!',
        'content': '''
        Feel free to browse around.
        I will open registration when everything is ready. &mdash; <b>admin</b>
        ''',
    },
    '54ef5f89-5c12-4d0a-a97b-9c367a8f46fb': {
        'user': 'guest',
        'topic': 'This is an example note.',
        'content': 'This is the content of an example note.',
    },
    'f37f9963-4393-4a75-be21-1c60b274d827': {
        'user': 'admin',
        'topic': 'Testing testing',
        'content': 'This is a test for saving new notes.',
    },
    'd0e261ce-ba5d-4a00-9781-a011017ea6dc': {
        'user': 'admin',
        'topic': 'Using Fetch API',
        'content': '''
        <a href="https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API">
        https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
        </a>
        ''',
    },
    '8471828f-dbec-4fe0-a7db-eed57b39b1fa': {
        'user': 'admin',
        'topic': 'Flag',
        'content': r'''
<p>Congratulations! Here are some cows for you.</p>
<pre>
          (__)
          (oo)                       U
   /-------\/                    /---V
  / |     ||                    * |--|                       .
 *  ||----||
    ^^    ^^

 Cow at 1 meter.         Cow at 100 meters.        Cow at 10,000 meters.
</pre>
        ''',
    },
}
