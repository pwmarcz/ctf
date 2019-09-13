from flask import Flask, render_template, request
import time

app = Flask(__name__)

# ''.join(random.choice('1234567890') for i in range(10))
PIN = '1328061477'

DELAY = 0.3


@app.route('/pin2/')
def pin():
    pin = request.args.get('pin')
    if pin:
        if compare(pin, PIN):
            return render_template('login.html', pin_correct=True)
        else:
            return render_template('login.html', pin_incorrect=True)
    return render_template('login.html')


def compare(pin1, pin2):
    m = max(len(pin1), len(pin2))
    for i in range(m):
        time.sleep(DELAY)
        if i >= len(pin1) or i >= len(pin2):
            return False
        if pin1[i] != pin2[i]:
            return False
    return True
