import json
import urllib.request
import ssl

_BASE_URL = 'https://www.neural-guide.me/'

def post_request(data, suffix):
    context = ssl._create_unverified_context()
    req = urllib.request.Request(_BASE_URL + suffix)
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))

    response = urllib.request.urlopen(req, jsondataasbytes, context=context)

    if (suffix != 'add-intolerances' and suffix != 'add-preferences'):

        bytes_data = response.read()

        dictionary = json.loads(bytes_data)
        return dictionary

def get_something(what_to_get, uid):
    if what_to_get == "menu":
        out_dict = {
            'userID': uid,
        }
        print(post_request(
            data=out_dict,
            suffix='get-menu'
        ))
    elif what_to_get == "recipe":
        keywords = input("Any preferences?")
        out_dict = {
            'userID': uid,
            'keyword': keywords
        }

        print(post_request(
            data=out_dict,
            suffix='get-recipe'
        ))

def main():

    uid = -1
    login_success = False
    while (not login_success):
        username = input("Email: ")
        password = input("Password: ")

        login_dict = {
            'email': username,
            'password': password
        }

        result = post_request(
            data=login_dict,
            suffix='foodbot/login'
        )

        login_success = result['success']
        if login_success:
            uid = result['userID']
        else:
            print("Login Failed! Try again")

    print("Login successful!")

    what_to_get = input("What can I help you with today?")

    get_something(what_to_get, uid)

    while (True):
        feedback = input("Anything else?")
        if feedback == "no":
            print("Okay! Goodbye!")
            return
        get_something(feedback, uid)



def create_user():
    out_dict = {
        'userID': 1,
        'gender': 'M',
        'date_of_birth': '1996-02-20',
        'activity_level': 2,
        'target': 'lose'
    }

    post_request(
        data=out_dict,
        suffix='signup2'
    )

    out_dict = {
        'userID': 1,
        'preferences': ['vegan']
    }

    post_request(
        data=out_dict,
        suffix='add-preferences'
    )

    out_dict = {
        'userID': 1,
        'intolerances': ['Lactose', 'Egg', 'Stuff', 'Soy']
    }

    post_request(
        data=out_dict,
        suffix='add-intolerances'
    )

if __name__ == "__main__":
    create_user()
    main()