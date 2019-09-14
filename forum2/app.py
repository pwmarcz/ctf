from flask import Flask, render_template, request, redirect
import os
import contextlib
import sqlite3


app = Flask(__name__)

POST_COLUMNS = ['id', 'user', 'topic', 'content', 'deleted']


@app.route('/forum2/')
def posts():
    with connect() as conn:
        user = request.args.get('user')

        c = conn.cursor()
        if user:
            c.execute(f"SELECT * FROM posts WHERE deleted = 0 AND user = '{user}'")
        else:
            c.execute('SELECT * FROM posts WHERE deleted = 0')

        posts = [dict(zip(POST_COLUMNS, p)) for p in c.fetchall()]
        print(posts)
        return render_template('forum.html', posts=posts, user=user)


@contextlib.contextmanager
def connect():
    conn = sqlite3.connect(':memory:')
    initdb(conn)
    try:
        yield conn
    finally:
        conn.close()


def initdb(conn):
    c = conn.cursor()
    c.execute('''
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        user TEXT,
        topic TEXT,
        content TEXT,
        deleted INTEGER
    );
    ''')
    c.executemany('''
    INSERT INTO posts (user, topic, content, deleted)
    VALUES (?, ?, ?, ?);
    ''', INIT_POSTS)
    conn.commit()


INIT_POSTS = [
    ('admin', 'Testing...', 'Is the new database working?', 0),
    ('hamlet1', 'Yeah!', 'Seems to work! And we have <b>formatting</b> <i>options</i> too.', 0),
    ('lorem', 'Lorem ipsum',
     ''' Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Proin dictum,
     turpis eu venenatis congue, erat mauris varius tellus, vel imperdiet justo
     tortor at lacus.  Fusce pellentesque augue ligula, quis tempus ex
     fringilla vel. Mauris ullamcorper euismod feugiat. Vestibulum ante ipsum
     primis in faucibus orci luctus et ultrices posuere cubilia Curae; In in
     pulvinar neque, nec varius dui. Maecenas eleifend molestie sem sit amet
     efficitur. Curabitur faucibus efficitur augue vitae porttitor. Aliquam
     ultricies nisl ultricies suscipit suscipit. Vestibulum vitae dolor
     risus. Fusce quis ante ex.  ''', 0),
    ('admin', 'Lorem, do not spam.', "I'm going to delete your posts.", 0),
    ('admin', 'Flag: Secret post',
     r'''
<pre>
 ____________________________________
/ Only the dead have seen the end of \
| cyberwar.                          |
|                                    |
\ - InfoSec Taylor Swift             /
 ------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
</pre>
     ''', 1),
    ('admin', 'Announcements', """
    Hi,<br>
    I finished some new features today:
    <ul>
      <li>
        Posts can be deleted (actually, only marked as deleted).
        Thanks to Hamlet1 who showed me that I can just do
        <tt>SELECT * FROM posts WHERE deleted = 0</tt>. I already used the
        feature to delete some secret info posted by mistake!
      <li>
        You can filter posts by user's name. This wasn't easy but I think I
        finally got the SQL right.
    </ul>
    """, 0),
    ('hamlet1', 'Glad I could help!', 'SQL is not that hard once you get to know it.', 0),
    ('admin', 'Somebody is hacking my system!',
     "Sorry, I'm disabling login for now.", 0),
]
