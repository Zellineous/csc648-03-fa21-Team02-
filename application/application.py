from flask import Flask, render_template, request, redirect, url_for, session
import pymysql


application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'

conn = pymysql.connect(
        host= 'team2-database.c8md5pg3obvk.us-west-1.rds.amazonaws.com', 
        port = 3306,
        user = 'csc64803team2', 
        password = 'password123',
        db = 'tutorDB',
        cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()

# in .html files, make sure to href= to these routes, not the location of the .html files themselves
@application.route('/', methods=['GET','POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        search = request.form.get('search')
        search_category = request.form.get('search_category')
        return redirect(url_for('results', search=search, search_category=search_category))

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
    search_category = request.args.get('search_category',None)
    print(search_category)
    if search_category == 'Subject':
        cursor.execute("SELECT name, subject, number FROM course WHERE subject  LIKE '%" + search + "%';")
    elif search_category == 'Class':
        cursor.execute("SELECT name, subject, number FROM course WHERE name LIKE '%" + search + "%';")
    else:
        cursor.execute("SELECT name, subject, number FROM course WHERE name  LIKE '%" + search + "%' OR CONCAT(subject, ' ' , number) LIKE '%" + search + "%';") # query to get from database from searching
    
    data = cursor.fetchall()    
    names = []      # e.g. 'software engineering'
    codes = []      # e.g. csc 648
    for course in data:
        print(course)
        names.append(course[0])
        codes.append(course[1] + ' ' + course[2])
    length = len(codes)

    return render_template('results.html', search=search, names=names, codes=codes, len=length)


@application.route('/team/<member>_about')
def team_member_about(member):
    return render_template('team/' + member + '.html')




@application.route('/tutor')
def tutor():
    return render_template('tutor.html')

@application.route('/editprofile')
def editprofile():
    return render_template('editprofile.html')




@application.route('/register')
def register():
    return render_template('register.html')

@application.route('/register', methods=['POST'])
def register_post():
    # TODO: validate and add user to database
    return redirect('dashboard.html')




@application.route('/login', methods =['GET', 'POST'], strict_slashes=False)
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')




# alberto - implement
@application.route('/search')
def search():
    return render_template('search.html')



# shailendra - implement
# @application.route('/messages')
# def messages():
#     return render_template('message.html')

@application.route('/inbox')
def inbox():
    return render_template('inbox.html')

# shailendra - implement
@application.route('/message')
def message():
    return render_template('message.html')# shailendra - implement
@application.route('/messages', methods = ['GET','POST'])
def messages():
    if request.method == "POST":
        message = request.form.get("message")
        print(message)
    return render_template('messages.html')

if __name__ == '__main__':
    application.run(debug=True)
