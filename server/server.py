from flask import Flask, request, jsonify, json, Response
import urllib
import ssl
from DatabaseHandler import DatabaseHandler as Dh

_API_KEY = "JTNTukkrHomshtW9HthnNtHgevJop1SkQ2FjsnY2JgDdYDoS77"

app = Flask(__name__)

dh = Dh("food_bot")


@app.route("/add-diseases", methods=["POST"])
def add_diseases():
    if request.is_json:
        data = request.json
        if len(data) == 2 and \
                        'userID' in data and \
                        'diseases' in data:
            dh.add_diseases(userID=data['userID'], preferences=data['diseases'])

            return Response(response="Success", status=200)

    else:
        return Response(response="Expected JSON", status=400)


@app.route("/add-intolerances", methods=["POST"])
def add_intolerances():
    if request.is_json:
        data = request.json
        if len(data) == 2 and \
                        'userID' in data and \
                        'intolerances' in data:
            dh.add_intolerances(userID=data['userID'], preferences=data['intolerances'])

            return Response(response="Success", status=200)

    else:
        return Response(response="Expected JSON", status=400)


@app.route("/add-preferences", methods=["POST"])
def add_prefs():
    if request.is_json:
        data = request.json
        if len(data) == 2 and \
                'userID' in data and \
                'preferences' in data:

            dh.add_preferences(userID=data['userID'], preferences=data['preferences'])

            return Response(response="Success", status=200)

    else:
        return Response(response="Expected JSON", status=400)


@app.route("/signup2", methods=["POST"])
def signup2():
    if request.is_json:
        data = request.json
        if len(data) == 3 and \
                        'userID' in data and \
                        'gender' in data and \
                        'date_of_birth' in data and \
                        'activity_level' in data and\
                        'target' in data:

            success = dh.signup_step_two(
                userID=data['userID'],
                gender=data['gender'],
                date_of_birth=data['date_of_birth'],
                activity_level=data['activity_level'],
                target=data['target']
            )

            result = dict()

            result['success'] = success

            return jsonify(result)

    else:
        # error
        return Response(response="Expected JSON", status=400)


@app.route("/signup1", methods=["POST"])
def signup1():
    if request.is_json:
        data = request.json
        if len(data) == 3 and \
            'email' in data and \
            'password' in data and \
            'name' in data:

            uID, success = dh.signup_step_one(data['email'], data['password'], data['name'])

            result = dict()

            result['userID'] = uID
            result['success'] = success

            return jsonify(result)

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

            print(result)

            return jsonify(result)

    else:
        #error
        return Response(response="Expected JSON", status=400)


@app.route("/get-todays-menu",methods=['POST'])
def get_todays_menu():
    context = ssl._create_unverified_context()

    if request.is_json:
        userID = request.json['userID']
    else:
        return Response(response="Expected JSON", status=400)

    intolerances = dh.get_intolerances(userID)
    diet = dh.get_preferences(userID)
    targetCalories = dh.get_kcal_per_day(userID)
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

    dictionary_result = json.loads(data)

    return jsonify(dictionary_result)

@app.route("/get-recipe",methods=['POST'])
def get_recipe():
    context = ssl._create_unverified_context()

    if request.is_json:
        data = request.json
        if len(data) == 2 and 'keyword' in data:
            userID = data['userID']
            keyword = data['keyword']

    intolerances = dh.get_intolerances(userID=userID)
    diet = dh.get_preferences(userID)
    targetCalories = int(dh.get_kcal_per_day(userID) / 3)
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

    dictionary_result = json.loads(data)

    return jsonify(dictionary_result)


@app.route("/")
def home():
    return "Hello world!"

if __name__ == "__main__":
    app.run(debug=True)