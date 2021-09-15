from flask import Flask, render_template

application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'


@application.route('/')
def home():
    return '<h2>Hello,</h2> This is the home page. and it works with html'


if __name__ == '__main__':
    application.run(debug=True)
