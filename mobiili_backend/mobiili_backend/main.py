from flask import Flask
from flask import jsonify
from flask import abort
import json
import MySQLdb
from flask import request
from hashlib import md5
from functools import wraps
from flask import session
from flask import make_response
from werkzeug.utils import secure_filename
from flask import send_from_directory

IMAGE_FOODS = '/home/ubuntu/images/food/'
IMAGE_DRINKS = '/home/ubuntu/images/drink/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['IMAGE_FOODS'] = IMAGE_FOODS
app.config['IMAGE_DRINKS'] = IMAGE_DRINKS

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index():
        abort(418)
        #return "index"

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
    invalidPassword = make_response("Invalid Password")
    loginerror = make_response("invalid username or passord")
    jsonuser = str(username_form)
    jsonpass = str(password_form)

     
    try:
        cursor.execute( """SELECT Username FROM User WHERE Username = %s""", (jsonuser,))
        userss = str(cursor.fetchone()[0])
    except:
        return invalidUser
    
    try:
        cursor.execute("""SELECT Password FROM User WHERE Username = %s""", (jsonpass,)) 
        pass2 = str(cursor.fetchone()[0])     
    except:
        return invalidPassword

  
    if jsonuser == userss and jsonpass == pass2:
        token = userss

        #Put it in the session
        session['api_session_token'] = token
        return okresp
    else:
        return loginerror
    return app.response_class(content_type='application/json')


@app.route('/food_img/<filename>')
def show_image_food(filename):
    return send_from_directory(app.config['IMAGE_FOODS'],
                               filename)
@app.route('/drink_img/<filename>')
def show_image_drink(filename):
    return send_from_directory(app.config['IMAGE_DRINKS'],
                               filename)


@app.route('/foods', methods=['GET', 'POST'])
#@require_api_token
def foods():
    if request.method == 'POST':
        if not request.json:
            abort(400)

            url = 'http://ec2-35-167-155-40.us-west-2.compute.amazonaws.com/food_img/'


            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
            return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['IMAGES_FOODS'], filename))
                return redirect(url_for('uploaded_file',
                                    filename=filename))


            cursor = db.cursor()
            IMG_URL = url + filename
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
#@require_api_token
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
