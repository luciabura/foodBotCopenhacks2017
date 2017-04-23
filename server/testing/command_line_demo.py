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

    bytes_data = response.read()

    dictionary = json.loads(bytes_data)
    return dictionary


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

    if what_to_get == "menu":
        out_dict = {
            'userID': uid,
        }
        print(post_request(
            data=out_dict,
            suffix='get-menu'
        ))

if __name__ == "__main__":
    main()