from flask import Flask, render_template, request, redirect, url_for, session
import database as db
import re
import helpers
import datetime

application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'
conn = db.connect()
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
    print("SEARCH CATEGORY " + search_category)
    return render_template('browse.html', search=search, names=names, codes=codes, len=length)


@application.route('/team/<member>_about')
def team_member_about(member):
    return render_template('team/' + member + '.html')


@application.route('/tutor', methods =['GET', 'POST'])
def tutor():
    username = request.args.get('user')
    user = helpers.getUserData(username)
    id = user['sfsu_id']
    user_profile = helpers.getUserProfile(id)

    if user_profile:
        name = user_profile['name']
        major = user_profile['major']
        # class = user_profile['class']
        phone = user_profile['phone']
        status = user_profile['status']
        avail = user_profile['availability']
        email = user['sfsu_email']
        gender = user_profile['gender']


    return render_template('tutor.html', name=name, major=major, phone=phone, status=status, 
        availability=avail, email=email, gender=gender)




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
            makeUserProfile(sfsu_id)
            msg = 'You have successfully registered!'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@application.route('/login', methods =['GET', 'POST'], strict_slashes=False)
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        

        password = request.form['password']
        account = helpers.getUserData(username)
        if account:
            #print(account)
            if(helpers.checkPasswordOfUser(username,password)):
                session['loggedin'] = True
                session['id'] = account['sfsu_id']
                session['username'] = account['name']
                msg = 'Logged in successfully!'
                return render_template('dashboard.html', msg = msg)
            else:
                msg = 'Incorrect username or password!'
        else:
            msg = 'Account does not exist!'
    return render_template('login.html', msg = msg)


@application.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')


@application.route('/dashboard', methods =['GET', 'POST'])
def dashboard():
    print(request.method)
    return render_template('dashboard.html')




# alberto - implement
@application.route('/search')
def search():
    return render_template('search.html')




@application.route('/inbox', methods =['GET', 'POST'])
def inbox():
    data = request.args.get('user')
    data = helpers.getUserData(data)
    print(data)
    user_id = data['sfsu_id']
    print(user_id)
    #get list of all users that have sent a message
    cursor.execute(f"SELECT * FROM message WHERE id IN (SELECT MAX(id) FROM message GROUP BY conversation)")
    messages = cursor.fetchall()
    print("messages from: ")
    print(messages)
    people = [] #penpal?
    lastMessages = []
    dates = []
    conversations = []
    lastSenders = []
    #get conversation partner names
    for message in messages:
        convoID = message['conversation']
        print(f"conversation # {convoID}")
        cursor.execute(f"SELECT * FROM conversation WHERE id={convoID}")
        conversations.append(cursor.fetchone())
    
    
    print(conversations)
    for convo in conversations:
        if convo['user1'] == user_id:
            cursor.execute(f"SELECT name FROM user WHERE sfsu_id={convo['user2']}")
            name = cursor.fetchone()['name']
            people.append(name)
        elif convo['user2'] == user_id:
            cursor.execute(f"SELECT name FROM user WHERE sfsu_id={convo['user1']}")
            name = cursor.fetchone()['name']
            people.append(name)
    for message in messages:
        dates.append(message['datetime'].strftime('%Y-%m-%d %H:%M:%S'))
        lastMessages.append(message['message'])
        cursor.execute(f"SELECT name FROM user WHERE sfsu_id={message['sending_user']}")
        lastSenders.append(cursor.fetchone()['name'])
        
    #get only most recent message from another user

    

    return render_template('inbox.html', people=people,dates=dates,lastMessages=lastMessages,len=len(people),lastSenders=lastSenders)

@application.route('/messaging', methods =['GET', 'POST'])
def messaging():
    toUser = helpers.getUserData(session['username'])


    return render_template('messaging.html')

@application.route('/viewmessage')
def viewmessage():
    return render_template('viewmessage.html')
    



if __name__ == '__main__':
    application.run(debug=True)
