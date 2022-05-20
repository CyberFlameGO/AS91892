from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    deez ;ntus
    :return:
    """
    return str(request.args)


if __name__ == '__main__':
    app.run()
