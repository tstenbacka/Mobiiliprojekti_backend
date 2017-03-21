from flask import Flask
from flask import jsonify
import random
app = Flask(__name__)

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
        foods = [
            {
                'id' : 1 ,
                'IMG_URL' : "http://vignette3.wikia.nocookie.net/meme/images/c/c7/Fd665178b5.jpg/revision/latest?cb=20160524214933",
                'food_name' : "hernari" ,
                'description' : "hernari"
             },
             {
                'id' : 2 ,
                'IMG_URL' : "http://vignette3.wikia.nocookie.net/meme/images/c/c7/Fd665178b5.jpg/revision/latest?cb=20160524214933",
                'food_name' : "gorilla" ,
                'description' : "gorilla lihabullia"
             }
        ]
        
        return jsonify(foods)

@app.route('/foods/<id>')
def food(id):
        return jsonify(
        id = "%s" %id ,
        IMG_URL = "http://vignette3.wikia.nocookie.net/meme/images/c/c7/Fd665178b5.jpg/revision/latest?cb=20160524214933" ,
        food_name = "hernari" ,
        description = "hernari"
        )

@app.route('/drinks')
def drinks():
        drinks = [
            {
                'id' : 1 ,
                'IMG_URL' : "http://vignette3.wikia.nocookie.net/meme/images/c/c7/Fd665178b5.jpg/revision/latest?cb=20160524214933" ,
                'drink_name' : "santtu" ,
                'description' : "Suomen yliarvostetuin olut"
            } ,
            {
                'id' : 2 ,
                'IMG_URL' : "http://vignette3.wikia.nocookie.net/meme/images/c/c7/Fd665178b5.jpg/revision/latest?cb=20160524214933" ,
                'drink_name' : "Koff" ,
                'description' : "Jumalten juoma"              
            }
        ]
        return jsonify(drinks)

@app.route('/drinks/<id>')
def drink(id):
        return jsonify(
        id = "%s" %id ,
        IMG_URL = "http://vignette3.wikia.nocookie.net/meme/images/c/c7/Fd665178b5.jpg/revision/latest?cb=20160524214933" ,
        drink_name = "santtu" ,
        description = "Suomen yliarvostetuin olut"
        )

if __name__ == "__main__":
    app.run()
