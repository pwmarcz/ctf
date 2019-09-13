from flask import Flask, render_template, request, session, Response, redirect, url_for, flash
import random
import base64


app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/mines/'
app.secret_key = 'minesweeper!'


WIDTH = 8
HEIGHT = 8
MINES = 10


def array2d(val):
    return [[val for x in range(WIDTH)] for y in range(HEIGHT)]


def make_new_game():
    mines = array2d(0)
    visible = array2d(0)

    for i in range(MINES):
        while True:
            x = random.randrange(WIDTH)
            y = random.randrange(HEIGHT)
            if (x, y) != (0, 0) and not mines[y][x]:
                mines[y][x] = 1
                break

    labels = make_labels(mines)

    return {'mines': mines, 'labels': labels, 'visible': visible, 'state': 'playing'}


def make_labels(mines):
    labels = array2d(0)
    for y in range(WIDTH):
        for x in range(HEIGHT):
            total = 0
            for y1, x1 in around(y, x):
                total += mines[y1][x1]
            labels[y][x] = total
    return labels


@app.route('/mines/')
def mines():
    if 'game' in session:
        game = session['game']
        new_game = False
    else:
        game = session['game'] = make_new_game()
        new_game = True

    game = session['game']
    try:
        return render_template(
            'mines.html',
            game=game,
            range_y=range(HEIGHT),
            range_x=range(WIDTH),
            game_base64=serialize(game),
        )
    except Exception as e:
        if new_game:
            raise
        flash(f'Something went wrong: {e!r}. Resetting game.')
        del session['game']
        return redirect(url_for('mines'))


@app.route('/mines/new/')
def new_game():
    session['game'] = make_new_game()
    return redirect(url_for('mines'))


@app.route('/mines/reveal/<int:y>/<int:x>')
def reveal(y, x):
    game = session['game']
    if y < 0 or y >= HEIGHT or x < 0 or x >= WIDTH:
        return Response('Out of bounds', status=400)

    if game['mines'][y][x]:
        game['state'] = 'dead'
    else:
        do_reveal(game, y, x)
        num_visible = sum(map(sum, game['visible']))
        if num_visible >= WIDTH * HEIGHT - MINES:
            game['state'] = 'win'

    session['game'] = game
    return redirect(url_for('mines'))


@app.route('/mines/load/', methods=['POST'])
def load():
    try:
        game_base64 = request.form.get('game_base64')
        message, game = deserialize(game_base64)
        session['game'] = game
        flash(message)
    except Exception as e:
        flash(f'Error loading game: {e!r}')
    return redirect(url_for('mines'))


def do_reveal(game, y, x):
    if game['visible'][y][x]:
        return

    game['visible'][y][x] = 1
    if game['labels'][y][x] == 0:
        for y1, x1 in around(y, x):
            do_reveal(game, y1, x1)


def around(y, x):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            y1 = y + dy
            x1 = x + dx
            if (y1 != y or x1 != x) and (0 <= x1 < WIDTH) and (0 <= y1 < HEIGHT):
                yield y1, x1


def serialize(game):
    message = 'Successfully loaded!'
    r = repr(message) + ',' + repr(game).replace(' ', '')
    return base64.b64encode(r.encode('ascii')).decode('ascii')


def deserialize(game_base64):
    r = base64.b64decode(game_base64)
    return eval(r)
