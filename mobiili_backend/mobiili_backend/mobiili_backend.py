from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
import MySQLdb
#import json

app = Flask(__name__)

# add here the actual DB info
# db = MySQLdb.connect("127.0.0.1", "root", "asd", "Mobiili")
db = MySQLdb.connect("127.0.0.1", "root", "asd", "Mobiili")

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
        return request.json

@app.route('/foods', methods=['GET', 'POST'])
def foods():
        if request.method == 'POST':
            if not request.json:
                abort(400)

            cursor = db.cursor()
            IMG_URL = db.escape_string(request.json["IMG_URL"])
            description = request.json['description']
            food_name = request.json['food_name']
    
            sql = ("INSERT INTO FOOD_RECIPES (food_name, Description, IMG_URL) VALUES (%s,%s,%s) ")

            dataToDB = (food_name,description,IMG_URL)        

            try:
	            # Execute dml and commit changes
                cursor.execute(sql,dataToDB)
                db.commit()    
            except:
	            # Rollback changes
                db.rollback()
                abort(500)
                
            return jsonify(request.json), 201

        else:
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

@app.route('/foods/<id>', methods=['GET'])
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
        if request.method == 'POST':
            if not request.json:
                abort(400)
            cursor = db.cursor()
            IMG_URL = db.escape_string(request.json["IMG_URL"])
            description = request.json['description']
            drink_name = request.json['drink_name']
    
            sql = ("INSERT INTO DRINK_RECIPES (Drink_name, Descripsion, IMG_URL) VALUES (%s,%s,%s) ")

            dataToDB = (drink_name,description,IMG_URL)        

            try:
	            # Execute dml and commit changes
                cursor.execute(sql,dataToDB)
                db.commit()    
            except:
	            # Rollback changes
                db.rollback()
                abort(500)
                
            return jsonify(request.json), 201


        else:
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

@app.route('/drinks/<id>', methods=['GET'])
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
