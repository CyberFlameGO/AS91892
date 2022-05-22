from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/meme')
def hello_world():
    """
    deez ;ntus
    :return:
    """
    return ' '.join([*request.args.to_dict()])

@app.route('/')
def hello_uwu():
    return render_template("index.html")

@app.route('/contact')
def hello_owo():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run()
