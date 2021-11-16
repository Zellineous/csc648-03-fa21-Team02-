from flask import Flask, render_template, request, redirect, url_for

application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'


# in .html files, make sure to href= to these routes, not the location of the .html files themselves
@application.route('/', methods=['GET','POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        print(request.form)
        search = request.form.get('search')
        return redirect(url_for('results', search=search))

    return render_template('home.html')


@application.route('/about')
def about():
    return render_template('about.html')


@application.route('/browse')
def browse():
    return render_template('browse.html')


@application.route('/results', methods=['GET', 'POST'])
def results():
    search = request.args.get('search',None)
    return render_template('results.html', search=search)


@application.route('/team/<member>_about')
def team_member_about(member):
    return render_template('team/' + member + '.html')


@application.route('/register')
def register():
    return render_template('register.html')


@application.route('/login/')
def login():
    return render_template('index.html')


@application.route('/test')
def hometest():
    return render_template('test.html')

if __name__ == '__main__':
    application.run(debug=True)
