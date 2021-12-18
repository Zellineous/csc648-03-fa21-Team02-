from flask import Flask, render_template, request, redirect, url_for, session
import database as db
import re
import helpers

application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'
conn = db.connect()
cursor = conn.cursor()
print(helpers.key)
# in .html files, make sure to href= to these routes, not the location of the .html files themselves
@application.route('/', methods=['GET','POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        search = request.form.get('search')
        search_category = request.form.get('search_category')
        return redirect(url_for('results', search=search, search_category=search_category))

    return render_template('home.html')


@application.route('/layout', methods=['GET','POST'])
def nav_search():
    print(request.method)
    if request.method == 'POST':
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



@application.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'sfsu_id' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        sfsu_id = request.form['sfsu_id']
        cursor.execute(f"SELECT sfsu_id FROM user WHERE name='{username}' OR sfsu_id={sfsu_id} OR sfsu_email='{email}'")
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not helpers.isValidSfsuEmail(email):
            msg = 'Invalid email address! Enter your SFSU email'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute(f"INSERT INTO user (name,password,sfsu_email,sfsu_id) VALUES ('{username}','{helpers.encryptPass(password)}','{email}','{sfsu_id}')")
            conn.commit()
            msg = 'You have successfully registered !'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@application.route('/login', methods =['GET', 'POST'], strict_slashes=False)
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if(helpers.checkPasswordOfUser(username,password)):
            cursor.execute(f"SELECT * FROM user WHERE name='{username}'")
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['sfsu_id']
                session['username'] = account['name']
                msg = 'Logged in successfully !'
                return render_template('dashboard.html', msg = msg)
            else:
                msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@application.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')


@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')




# alberto - implement
@application.route('/search')
def search():
    return render_template('search.html')




@application.route('/inbox')
def inbox():
    return render_template('inbox.html')

@application.route('/messaging')
def messaging():
    return render_template('messaging.html')
    



if __name__ == '__main__':
    application.run(debug=True)
