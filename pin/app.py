from flask import Flask, render_template, request
import time

app = Flask(__name__)

PIN = '7532'


@app.route('/')
def pin():
    pin = request.args.get('pin')
    if pin:
        if pin == PIN:
            return render_template('login.html', pin_correct=True)
        else:
            return render_template('login.html', pin_incorrect=True)
    return render_template('login.html')
