from flask import Flask
from flask import jsonify
import random
app = Flask(__name__)

@app.route('/')
def index():
        return jsonify(
        temperature=random.randint(-35, 40) ,
	humidity=random.randint(5, 90)
    )

if __name__ == "__main__":
    app.run()
