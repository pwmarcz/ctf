from flask import Flask, render_template, request, session, Response, redirect, url_for
import random


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
    if 'game' not in session:
        session['game'] = make_new_game()

    game = session['game']
    # uncover(game, 0, 0)
    return render_template('mines.html', game=game, range_y=range(HEIGHT), range_x=range(WIDTH))


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
