from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/spots', methods=['GET', 'POST'])
def spots():
    if request.method == 'POST':
        return "dedede"
    else:
        return check_available_spots()

def check_available_spots():
    return "no spots for you!"