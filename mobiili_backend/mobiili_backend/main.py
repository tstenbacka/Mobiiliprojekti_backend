from flask import Flask
from flask import jsonify
import MySQLdb
import json
from flask import request

app = Flask(__name__)

# add here the actual DB info
# db = MySQLdb.connect("127.0.0.1", "root", "asd", "Mobiili")
db = MySQLdb.connect("127.0.0.1", "root", "mobiili", "Mobiili")

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
    
        sql = ("INSERT INTO User (Firstname, Lastname, Username, Email, Password) VALUES (%s,%s,%s,%s,%s) ")

        data_tiedot = (firstname,lastname,username,email,password)        
 
	try:
	    # Execute dml and commit changes
		cursor.execute(sql,data_tiedot)
		db.commit()    
	except:
	    # Rollback changes
		db.rollback()
        return app.response_class(content_type='application/json')
@app.route('/login', methods=['POST'])
    cursor = db.cursor()
    data = request.json
    username_form  = request.form['username']
    password_form  = request.form['password']
    cur.execute("SELECT COUNT(1) FROM users WHERE name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
    if cur.fetchone()[0]:
        cur.execute("SELECT pass FROM users WHERE name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
        for row in cur.fetchall():
            if md5(password_form).hexdigest() == row[0]:
                session['username'] = request.form['username']
            else:
                error = "Invalid Credential"
    else:
            error = "Invalid Credential"
return app.response_class(content_type='application/json')
 
@app.route('/foods', methods=['GET', 'POST'])
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
