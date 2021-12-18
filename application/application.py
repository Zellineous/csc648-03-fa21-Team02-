from flask import Flask, render_template, request, redirect, url_for, session
import database as db
import re
import helpers

application = Flask(__name__)
application.config['SECRET_KEY'] = '123456789'
conn = db.connect()
cursor = conn.cursor()

# in .html files, make sure to href= to these routes, not the location of the .html files themselves


@application.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        search = request.form.get('search')
        search_category = request.form.get('search_category')
        return redirect(url_for('results', search=search, search_category=search_category))

    return render_template('home.html')


@application.route('/layout', methods=['GET', 'POST'])
def nav_search():
    print(request.method)
    if request.method == 'POST':
        search = request.form.get('search')
        return redirect(url_for('results', search=search))

    return render_template('home.html')


@application.route('/about')
def about():
    return render_template('about.html')


# @application.route('/browse')
# def browse():
#     return render_template('browse.html')



@application.route('/layout', methods=['GET', 'POST'])
@application.route('/results', methods=['GET', 'POST'])
def results():
    search = request.args.get('search', None)
    search_category = request.args.get('search_category', None)

    print(search, search_category)
    if search_category == 'Majors':
        print('case1')
        if search:
            data = helpers.getSearch(search)
        else:
            data = helpers.getAllCourses()

    elif search_category:
        print('case2')
        major = helpers.getMajor(search_category)
        major_id = major['id']
        data = helpers.getAllCoursesFromMajor(major_id)

    elif search and search_category:
        print('case3')
        major = helpers.getMajor(search_category)
        major_id = major['id']
        data = helpers.getAllCoursesFromMajor(major_id)
        print(data)

    elif not search_category:
        print('case4')
        if search:
            data = helpers.getSearch(search)
        else:
            data = helpers.getAllCourses()

    print(data)
    numResults = 0
    courseNames = []
    courseCodes = []
    usernames = []
    listings = []

    for course in data:
        tutors = helpers.getTutorsTeaching(course['id'])
        for tutor in tutors:
            listings.append({'courseName':course['name'], 'tutor' : tutor['name'], 'code' : course['code']})

    for listing in listings:
        courseNames.append(listing['courseName'])
        usernames.append(listing['tutor'])
        courseCodes.append(listing['code'])
        numResults+=1

    # for styling header in results.html
    if not search:
        search = 'all'
    if search_category == 'Majors':
        search_category = 'all majors'
    if not search_category:
        search_category = 'all majors'

    return render_template('results.html', search=search, search_category=search_category, len = numResults, courseNames = courseNames, usernames=usernames, courseCodes=courseCodes)


@application.route('/team/<member>_about')
def team_member_about(member):
    return render_template('team/' + member + '.html')


@application.route('/tutor', methods=['GET', 'POST'])
def tutor():
    username = request.args.get('user')
    user = helpers.getUserData(username)
    id = user['sfsu_id']
    user_profile = helpers.getUserProfile(id)
    session['message_to_name'] = user['name']
    username =  user['name']
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
        avail=avail, email=email, gender=gender,username=username)




@application.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    user_id = session['id']
    forms = ['name', 'gender', 'email', 'phone', 'major', 'availability',
        'about', 'experience', 'education']
    valid_forms = []
    values = []
    if request.method == 'POST':
        
        cnt = 0

        for f in forms:
            value = request.form.get(f , None)
            if value:
                print("value")
                values.append(value)
                valid_forms.append(cnt)
            cnt += 1    

        count = 0

        for v in values:
            sql = "UPDATE user_profile SET {0} = '{1}' WHERE sfsu_id={2}".format(forms[valid_forms[count]], v, user_id)
            count += 1
            cursor.execute(sql)
            conn.commit()

    return render_template('editprofile.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'sfsu_id' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        sfsu_id = request.form['sfsu_id']
        cursor.execute(
            f"SELECT sfsu_id FROM user WHERE name='{username}' OR sfsu_id={sfsu_id} OR sfsu_email='{email}'")
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
            cursor.execute(
                f"INSERT INTO user (name,password,sfsu_email,sfsu_id) VALUES ('{username}','{helpers.encryptPass(password)}','{email}','{sfsu_id}')")
            conn.commit()
            cursor.execute(
                f"INSERT INTO user_profile (name,sfsu_id) VALUE ('{username}',{sfsu_id})")
            conn.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@application.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']

        password = request.form['password']
        account = helpers.getUserData(username)
        if account:
            # print(account)
            if(helpers.checkPasswordOfUser(username, password)):
                session['loggedin'] = True
                session['id'] = account['sfsu_id']
                session['username'] = account['name']
                msg = 'Logged in successfully!'
                return render_template('dashboard.html', msg=msg)
            else:
                msg = 'Incorrect username or password!'
        else:
            msg = 'Account does not exist!'
    return render_template('login.html', msg=msg)


@application.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')


@application.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = session['username']
    user = helpers.getUserData(username)
    id = user['sfsu_id']
    user_profile = helpers.getUserProfile(id)
    name = user_profile['name']
    return render_template('dashboard.html', name=name)


# alberto - implement
@application.route('/search')
def search():
    return render_template('search.html')


@application.route('/inbox', methods=['GET', 'POST'])
def inbox():
    print(request.method)
    data = request.args.get('user')
    data = helpers.getUserData(data)
    print(data)
    user_id = data['sfsu_id']
    # print(user_id)
    # get list of all users that have sent a message
    cursor.execute(
        f"SELECT * FROM message WHERE id IN (SELECT MAX(id) FROM message GROUP BY conversation)")
    messages = cursor.fetchall()
    #print("messages from: ")
    # print(messages)
    people = []  # penpal?
    lastMessages = []
    dates = []
    conversations = []
    lastSenders = []
    # get conversation partner names
    for message in messages:
        convoID = message['conversation']
        # print(f"conversation # {convoID}")
        cursor.execute(f"SELECT * FROM conversation WHERE id={convoID}")
        conversations.append(cursor.fetchone())

    print(conversations)
    for convo in conversations:
        if convo['user1'] == user_id:
            cursor.execute(
                f"SELECT name FROM user WHERE sfsu_id={convo['user2']}")
            name = cursor.fetchone()['name']
            people.append(name)
        elif convo['user2'] == user_id:
            cursor.execute(
                f"SELECT name FROM user WHERE sfsu_id={convo['user1']}")
            name = cursor.fetchone()['name']
            people.append(name)
    for message in messages:
        dates.append(message['datetime'].strftime('%Y-%m-%d %H:%M:%S'))
        lastMessages.append(message['message'])
        cursor.execute(
            f"SELECT name FROM user WHERE sfsu_id={message['sending_user']}")
        lastSenders.append(cursor.fetchone()['name'])

    # get only most recent message from another user

    return render_template('inbox.html', people=people, dates=dates, lastMessages=lastMessages, len=len(people), lastSenders=lastSenders)


@application.route('/messaging', methods=['GET', 'POST'])
def messaging():
    user1 = helpers.getUserData(request.args.get('user'))['sfsu_id']
    user2 = helpers.getUserData(session['username'])['sfsu_id']
    print(helpers.getConversationMessages(user1, user2))

    return render_template('messaging.html')


@application.route('/viewmessage', methods=['GET', 'POST'])
def viewmessage():
    print(request.method)
    if request.method == 'POST':
        message = request.form.get('message')
        session['message'] = message                # message to send
        print(session['message'])
        receivingUser = session['message_to_name']  # receiver name
        sendingUser = session['username']           # sender name

        newMessage = helpers.createMessage(message,sendingUser,receivingUser)
        text = newMessage['message']
        
        userData = helpers.getUserData(receivingUser)
        userProfile = helpers.getUserProfile(userData['sfsu_id'])
        realName = userProfile['name']
        phone = userProfile['phone']
        major = userProfile['major']
        gender = userProfile['gender']
        

    else:
        username = request.args.get('user')
        text = request.args.get('message')
        
        userData = helpers.getUserData(username)
        userProfile = helpers.getUserProfile(userData['sfsu_id'])
        realName = userProfile['name']
        phone = userProfile['phone']
        major = userProfile['major']
        gender = userProfile['gender']
    

    return render_template('viewmessage.html',realName=realName,phone=phone,major=major,gender=gender,text=text)


if __name__ == '__main__':
    application.run(debug=True)
