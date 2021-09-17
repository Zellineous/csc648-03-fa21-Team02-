from flask import Flask, render_template
from string import Template

application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'

#in .html files, make sure to href= to these routes, not the location of the .html files themselves
@application.route('/')
@application.route('/home')
def home():
    return render_template('home.html')
@application.route('/about')
def about():
    return render_template('about.html')
@application.route('/thomas')
def thomas():
    return render_template('thomas.html')

@application.route('/team/<member>_about')
def team_member_about(member):
    return render_template('team/' + member + '.html')


if __name__ == '__main__':
    application.run(debug=True)
