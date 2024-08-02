
# from flask import Flask
# import os

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     message = os.getenv('WELCOME_MESSAGE', 'Hello, Welcome to KodeCamp DevOps Bootcamp!')
#    return f"<h1>{message}</h1>"

# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80)


import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    message = os.getenv('MESSAGE', 'Hello, Default!')
    return f"<h1>{message}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)