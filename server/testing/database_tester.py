from DatabaseHandler import DatabaseHandler as Dh
from datetime import datetime as dt

dh = Dh('../food_bot')

uid, success = dh.signup_step_one(
    email='test123@test.test',
    password='testTESTtest1',
    name='Mr Test1'
)

print(uid, success)

success = dh.signup_step_two(
    userID=uid,
    date_of_birth=dt.strptime('01-01-1996', '%d-%m-%Y'),
    gender='Male',
    activity_level=2,
    target='keep'
)

print(success)

success, uid, name = dh.try_to_login_user(
    email='test123@test.test',
    password='testTESTtest1',
)

print(success, uid)

success = dh.add_intolerances(userID=uid, intolerances=['Lactose', 'Egg', 'Stuff', 'Soy'])

dh.get_intolerances(uid)

success = dh.add_preferences(userID=uid, preferences=['Vegan'])

print(dh.get_preferences(uid))

print(dh.get_kcal_per_day(uid))