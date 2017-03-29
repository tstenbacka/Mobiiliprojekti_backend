from flask import Flask
from flask import jsonify
import MySQLdb
import json
from flask import request
from hashlib import md5
from functools import wraps
from flask import session
from flask import make_response

app = Flask(__name__)

# add here the actual DB info
# db = MySQLdb.connect("127.0.0.1", "root", "asd", "Mobiili")
db = MySQLdb.connect("127.0.0.1", "root", "mobiili", "Mobiili")

def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        resp = make_response ("Access Denied")
        # Check to see if it's in their session
        if 'api_session_token' not in session:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return resp

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_token


@app.route('/')
def index():
        return "index"

# password is NOT returned in the user JSON object
@app.route('/users/<id>')
def users(id):
        cursor = db.cursor()

        # execute SQL select statement
        cursor.execute("""SELECT * FROM User WHERE ID_user = %s""" %id)

        # commit your changes, apparently needed
        db.commit()

        rows = cursor.fetchall()

        for row in rows:
            t = (row[0], row[1], row[2], row[3])
            t = {
                'id' : row[0] ,
                'user_name' : row[3] ,
                'first_name' : row[1] ,
                'last_name' : row[2] ,
                'email' : row[4]            
                }
        return jsonify(t)
        # db close seems to break stuff (if we close the connection we should restart it so mayby we won't close it...) 
        # perhaps the connection should still be closed at some point?
        # db.close()
@app.route('/users', methods=['POST'])
def signup():
        cursor = db.cursor()
        data = request.json
        firstname = request.json['Firstname'],
       	lastname = request.json['Lastname'],
        username = request.json['Username'],
        email = request.json['Email'],
        password = request.json['Password']
        signResp = make_response ("sign up ok")
        sql = ("INSERT INTO User (Firstname, Lastname, Username, Email, Password) VALUES (%s,%s,%s,%s,%s) ")

        data_tiedot = (firstname,lastname,username,email,password)        
 
	try:
	    # Execute dml and commit changes
		cursor.execute(sql,data_tiedot)
		db.commit()
                return signResp
	except:
	    # Rollback changes
		db.rollback()
        return app.response_class(content_type='application/json')
@app.route('/login', methods=['POST'])
def login(): 
    cursor = db.cursor()
    data = request.json
    username_form  = request.json['Username']
    password_form  = request.json['Password']   
    okresp = make_response ("login ok")
    invalidUser = make_response("Invalid username")
    invalidPassword = make_response("Password")
   
 
    userQ = cursor.execute( """SELECT Username FROM User WHERE Username = '%s'""".format(username_form))
    passQ = cursor.execute("""SELECT Password FROM User WHERE Username = '%s'""".format(username_form))
 
    userss = str(userQ)    

    loginerror = make_response(userss)  
  
    if username_form == userQ and password_form == passQ:
        session['Username'] = request.form['Username']
        token = response['UseUsernamee']['authentication_token']

        # Put it in the session
        session['api_session_token'] = token
        return okresp
    else:
        return loginerror
    return app.response_class(content_type='application/json')
 
@app.route('/foods', methods=['GET', 'POST'])
@require_api_token
def foods():
	cursor = db.cursor()

        # execute SQL select statement
        cursor.execute("""SELECT * FROM FOOD_RECIPES""")

        # commit your changes, apparently needed
        db.commit()

        # get the number of rows in the resultset
        #  numrows = int(cursor.rowcount)
        rows = cursor.fetchall()
        rowarray_list = []

        for row in rows:
            t = (row[0], row[1], row[2], row[3])
            t = {
                'id' : row[0] ,
                'IMG_URL' : row[3] ,
                'food_name' : row[1] ,
                'description' : row[2]              
                }
            rowarray_list.append(t)
        return jsonify(rowarray_list)
        #db.close()

@app.route('/foods/<id>')
def food(id):
        cursor = db.cursor()

        # execute SQL select statement
        cursor.execute("""SELECT * FROM FOOD_RECIPES WHERE ID_food = %s""" %id)

        # commit your changes, apparently needed
        db.commit()

        rows = cursor.fetchall()

        for row in rows:
            t = (row[0], row[1], row[2], row[3])
            t = {
                'id' : row[0] ,
                'IMG_URL' : row[3] ,
                'food_name' : row[1] ,
                'description' : row[2]              
                }
        return jsonify(t)
        #db.close()

@app.route('/drinks', methods=['GET', 'POST'])
@require_api_token
def drinks():
        cursor = db.cursor()

        # execute SQL select statement
        cursor.execute("""SELECT * FROM DRINK_RECIPES""")

        # commit your changes, apparently needed
        db.commit()

        # get the number of rows in the resultset
        #  numrows = int(cursor.rowcount)
        rows = cursor.fetchall()
        rowarray_list = []

        for row in rows:
            t = (row[0], row[1], row[2], row[3])
            t = {
                'id' : row[0] ,
                'IMG_URL' : row[3] ,
                'drink_name' : row[1] ,
                'description' : row[2]              
                }
            rowarray_list.append(t)
        return jsonify(rowarray_list)
       # db.close()

@app.route('/drinks/<id>')
def drink(id):
        cursor = db.cursor()

        # execute SQL select statement
        cursor.execute("""SELECT * FROM DRINK_RECIPES WHERE ID_drink = %s""" %id)

        # commit your changes, apparently needed
        db.commit()

        rows = cursor.fetchall()

        for row in rows:
            t = (row[0], row[1], row[2], row[3])
            t = {
                'id' : row[0] ,
                'IMG_URL' : row[3] ,
                'drink_name' : row[1] ,
                'description' : row[2]              
                }
        return jsonify(t)
       # db.close()

if __name__ == "__main__":
    app.run()
