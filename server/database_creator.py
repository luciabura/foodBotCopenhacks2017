import sqlite3 as sql
from datetime import datetime, date

def execute_query(query):
    con = sql.connect("food_bot")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()

def create_credentials_table():
    query = "CREATE TABLE IF NOT EXISTS " \
            " credentials (" \
                " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                " userID INTEGER, " \
                " email VARCHAR(50), " \
                " pass VARCHAR(70)" \
             ")"
    execute_query(query)

def create_userData_table():
    query = "CREATE TABLE IF NOT EXISTS "\
            " userData (" \
            " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
            " name VARCHAR(50), " \
            " date_of_birth DATE, "\
            " gender VARCHAR(50), " \
            " activity_level INTEGER" \
            " target VARCHAR(50)" \
            ")"
    execute_query(query)

def create_intolerances_table():
    query = "CREATE TABLE IF NOT EXISTS " \
            " intolerances (" \
                " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                " name VARCHAR(50)" \
            ")"
    execute_query(query)

def create_userIntolerances_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " userIntolerances (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " userID INTEGER, " \
                    " intolID VARCHAR(50)" \
                ")"
    execute_query(query)

def create_diseases_table():
    query = "CREATE TABLE IF NOT EXISTS " \
            " diseases (" \
                " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                " name VARCHAR(50)" \
            ")"
    execute_query(query)

def create_userDiseases_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " userDiseases (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " userID INTEGER, " \
                    " disID INTEGER" \
                ")"
    execute_query(query)

def create_preferences_table():
    query = "CREATE TABLE IF NOT EXISTS " \
            " preferences (" \
                " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                " name VARCHAR(50)" \
            ")"
    execute_query(query)

def create_userPreferences_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " userPreferences (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " userID INTEGER, " \
                    " prefID INTEGER" \
                ")"
    execute_query(query)

def create_userHistory_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " userHistory (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " userID INTEGER, " \
                    " date DATE, " \
                    " recipe_ID INTEGER" \
                ")"
    execute_query(query)

def create_ageMapping_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " ageMapping (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " left_ageLimit INTEGER, " \
                    " right_ageLimit INTEGER " \
                ")"
    execute_query(query)

def create_kcal_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " kcal (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " age_group INTEGER, " \
                    " level INTEGER, " \
                    " kcal INTEGER " \
                ")"

def main():
    #(1) Creating credentials table
    create_credentials_table()
    #(2) Creating the user specific data table
    create_userData_table()

    create_preferences_table()

    create_userPreferences_table()

    create_diseases_table()

    create_userDiseases_table()

    create_intolerances_table()

    create_userIntolerances_table()

    create_userHistory_table()

    create_ageMapping_table()

    create_kcal_table()

if __name__ == "__main__":
    main()