from flask import Flask, request, jsonify, json, Response
import urllib
import ssl
from DatabaseHandler import DatabaseHandler as Dh
import hashlib
from passlib.hash import pbkdf2_sha256

_API_KEY = "JTNTukkrHomshtW9HthnNtHgevJop1SkQ2FjsnY2JgDdYDoS77"

app = Flask(__name__)

dh = Dh("food-bot")

@app.route("/signup1", methods=["POST"])
def signup1():
    if request.is_json:
        data = request.json
        if len(data) == 3 and \
            'email' in data and \
            'password' in data and \
            'name' in data:

            uID, success = dh.signup_step_one(data['email'], data['password'], data['name'])


    else:
        #error
        return Response(response="Expected JSON", status=400)

@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.json
        if len(data) == 2 and 'email' in data and 'password' in data:
            success, uID = dh.try_to_login_user(
                data['email'],
                data['password']
            )

            result = dict()
            result['success'] = success
            result['userID'] = uID

            return jsonify(result)

    else:
        #error
        return Response(response="Expected JSON", status=400)

@app.route("/get-todays-menu")
def get_todays_menu():
    context = ssl._create_unverified_context()

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/mealplans/generate?exclude=shellfish%2C+olives&targetCalories=2000&timeFrame=day"
    req = urllib.request.Request(url)
    req.add_header("X-Mashape-Key", _API_KEY)
    req.add_header("Accept", "application/json")

    data = urllib.request.urlopen(req, context=context).read()

    return data.decode()

@app.route("/")
def home():
    return "Hello world!"

if __name__ == "__main__":
    app.run(debug=True)