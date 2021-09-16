from flask import Flask, render_template
application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'


@application.route('/')
def home():
    return render_template('home.html')
@application.route('/about')
def about():
    return '<h2>this is the about PAGE,</h2> This is the home page. and it works with html, update from my own IDE'
@application.route('/thomas')
def thomas():
    return render_template('thomas.html')

if __name__ == '__main__':
    application.run(debug=True)
