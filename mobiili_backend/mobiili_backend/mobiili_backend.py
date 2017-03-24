from flask import Flask
from flask import jsonify
import MySQLdb

app = Flask(__name__)

# add here the actual DB info
# db = MySQLdb.connect("127.0.0.1", "root", "asd", "Mobiili")
db = MySQLdb.connect("127.0.0.1", "root", "asd", "Mobiili")

@app.route('/')
def index():
        return "index"

@app.route('/users/<id>')
def users(id):
        return jsonify(
        id = "%s" %id ,
        user_name = "test" ,
        first_name = "test" ,
        last_name = "test" ,
        email = "test@test.lol"
        )

@app.route('/users', methods=['POST'])
def signup():
        return request.json

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
        db.close()

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
        db.close()

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
        db.close()

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
        db.close()

if __name__ == "__main__":
    app.run()
