import pymysql.cursors
def connect():
    try:
        conn = pymysql.connect(
                                host= 'team2-database.c8md5pg3obvk.us-west-1.rds.amazonaws.com', 
                                port = 3306,
                                user = 'csc64803team2', 
                                password = 'password123',
                                db = 'tutorDB',
                                charset="utf8mb4",
                                cursorclass=pymysql.cursors.DictCursor )
        return conn
    except:
        print("error: could not connect to database...")