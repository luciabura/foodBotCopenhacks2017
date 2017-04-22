from flask import Flask
import urllib
import ssl

_API_KEY = "JTNTukkrHomshtW9HthnNtHgevJop1SkQ2FjsnY2JgDdYDoS77"

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    

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