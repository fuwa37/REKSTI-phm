from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():
    return 0

# app.run(host='0.0.0.0')
