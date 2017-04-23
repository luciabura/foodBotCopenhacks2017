from flask import Flask, request, jsonify, json, Response
import urllib
import ssl
from DatabaseHandler import DatabaseHandler as Dh
import hashlib
from passlib.hash import pbkdf2_sha256
import datetime

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
            success, uID, name = dh.try_to_login_user(
                data['email'],
                data['password']
            )

            result = dict()
            result['success'] = success
            result['userID'] = uID
            result['name'] = name

            return jsonify(result)

    else:
        #error
        return Response(response="Expected JSON", status=400)

@app.route("/get-recipe",methods=['POST'])
def get_recipe():
    context = ssl._create_unverified_context()

    if request.is_json:
        data = request.json
        if len(data) == 2 and 'keyword' in data:
            keyword = data['keyword']

    intolerances = dh.get_intolerances()
    diet = dh.get_preferences()
    targetCalories = dh.get_kcal()
    limitNumber = 5

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?"

    for i, val in enumerate(diet):
        if (i == 0):
            url += "diet="
        else:
            if (i != 0):
                url += "%2C+"
            url += val

    for i, val in enumerate(intolerances):
        if (i == 0):
            url += "&"
            url += "intolerances="
        else:
            if (i != 0):
                url += "%2C+"
            url += val

    if(targetCalories):
        url += "&maxCalories=" + targetCalories

    url += "&number=" + limitNumber

    if(keyword):
        url += "&query=" + keyword


    req = urllib.request.Request(url)
    req.add_header("X-Mashape-Key", _API_KEY)
    req.add_header("Accept", "application/json")

    data = urllib.request.urlopen(req, context=context).read()

    return data.decode()

@app.route("/get-week-menu",methods=['POST'])
def get_week_menu():
    context = ssl._create_unverified_context()

    intolerances = dh.get_intolerances()
    diet = dh.get_preferences()
    targetCalories = dh.get_kcal()
    timeFrame = 'week'

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/mealplans/generate?"

    for i, val in enumerate(diet):
        if (i == 0):
            url += "diet="
        else:
            if (i != 0):
                url += "%2C+"
            url += val

    for i, val in enumerate(intolerances):
        if (i == 0):
            url += "&"
            url += "exclude="
        else:
            if (i != 0):
                url += "%2C+"
            url += val

    if(targetCalories):
        url += "&targetCalories" + targetCalories

    url += "&timeFrame=" + timeFrame


    req = urllib.request.Request(url)
    req.add_header("X-Mashape-Key", _API_KEY)
    req.add_header("Accept", "application/json")

    data = urllib.request.urlopen(req, context=context).read()

    return data.decode()

@app.route("/get-todays-menu",methods=['POST'])
def get_todays_menu():
    context = ssl._create_unverified_context()

    intolerances = dh.get_intolerances()
    diet = dh.get_preferences()
    targetCalories = dh.get_kcal()
    timeFrame = 'day'

    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/mealplans/generate?"

    for i, val in enumerate(intolerances):
        if (i == 0):
            url += "&"
            url += "exclude="
        else:
            if (i != 0):
                url += "%2C+"
            url += val

    for i, val in enumerate(diet):
        if (i == 0):
            url += "&"
            url += "diet="
        else:
            if (i != 0):
                url += "%2C+"
            url += val

    if(targetCalories):
        url += "&" + targetCalories

    url += "&" + timeFrame


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