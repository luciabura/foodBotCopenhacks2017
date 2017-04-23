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
            " activity_level INTEGER, " \
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

def fill_intolerancesTable():
    query = "INSERT INTO intolerances(name) " \
                " VALUES ('Lactose'),('Egg'),('Gluten'),('Peanuts'),('Shellfish'),('Wheat'),('Yeast'),('Alcohol'),('Soy'),('Corn'),('Additives'),('Fructose')"
    execute_query(query)

def create_userIntolerances_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " userIntolerances (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " userID INTEGER, " \
                    " intolID INTEGER, " \
                    "UNIQUE(userID, intolID)" \
                ")"
    execute_query(query)

def create_diseases_table():
    query = "CREATE TABLE IF NOT EXISTS " \
            " diseases (" \
                " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                " name VARCHAR(50)" \
            ")"
    execute_query(query)

def fill_diseasesTable():
    query = "INSERT INTO diseases(name) " \
                " VALUES ('Diabetes'),('Candida'),('Salmonella'),('Hepatitis A'),('E. Coli'), ('Listeriosis')"
    execute_query(query)

def create_userDiseases_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " userDiseases (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " userID INTEGER, " \
                    " disID INTEGER, " \
                    "UNIQUE(userID, disID)" \
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
                    " prefID INTEGER, " \
                    "UNIQUE(userID, prefID)" \
                ")"
    execute_query(query)

def fill_preferencesTable():
    query = "INSERT INTO preferences(name) " \
                "VALUES ('Vegetarian'),('Vegan'),('Pescetarian'),('Lacto-Vegetarial'),('Ovo-Vegetarian'),('Dairy-Free'),('Paleo'),('Primal')"
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

def fill_ageMappingTable():
    query = "INSERT INTO ageMapping (left_ageLimit,right_ageLimit) " \
                " VALUES (16,18),(19,20),(21,25),(26,30),(31,35),(36,40),(41,45),(46,50),(51,55),(56,60),(61,75)"
    execute_query(query)

def create_kcal_table():
    query = "CREATE TABLE IF NOT EXISTS " \
                " kcal (" \
                    " id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    " age_group INTEGER, " \
                    " gender VARCHAR(50), " \
                    " level INTEGER, " \
                    " kcal INTEGER " \
                ")"
    execute_query(query)

def fill_kcal_table():
    query = " INSERT INTO kcal(age_group,gender,level,kcal) " \
                " VALUES (1,'F',1,1800),(1,'F',2,2000),(1,'F',3,2400)," \
                " (1, 'M', 1, 2400), (1, 'M', 2, 2800), (1, 'M', 3, 3200)," \
                " (2, 'F', 1, 2000), (2, 'F', 2, 2200), (2, 'F', 3, 2400)," \
                " (2, 'M', 1, 2600), (2, 'M', 2, 2800), (2, 'M', 3, 3200)," \
                " (3, 'F', 1, 2000), (3, 'F', 2, 2200), (3, 'F', 3, 2200)," \
                " (3, 'M', 1, 2400), (3, 'M', 2, 2800), (3, 'M', 3, 3000)," \
                " (4, 'F', 1, 2000), (4, 'F', 2, 2000), (4, 'F', 3, 2400)," \
                " (4, 'M', 1, 2400), (4, 'M', 2, 2600), (4, 'M', 3, 3000)," \
                " (5, 'F', 1, 1800), (5, 'F', 2, 2000), (5, 'F', 3, 2400)," \
                " (5, 'M', 1, 2400), (5, 'M', 2, 2600), (5, 'M', 3, 3000)," \
                " (6, 'F', 1, 1800), (6, 'F', 2, 2000), (6, 'F', 3, 2200)," \
                " (6, 'M', 1, 2400), (6, 'M', 2, 2600), (6, 'M', 3, 2800)," \
                " (7, 'F', 1, 1800), (7, 'F', 2, 2000), (7, 'F', 3, 2200)," \
                " (7, 'M', 1, 2200), (7, 'M', 2, 2600), (7, 'M', 3, 2800)," \
                " (8, 'F', 1, 1800), (8, 'F', 2, 2000), (8, 'F', 3, 2200)," \
                " (8, 'M', 1, 2200), (8, 'M', 2, 2400), (8, 'M', 3, 2800)," \
                " (9, 'F', 1, 1600), (9, 'F', 2, 2000), (9, 'F', 3, 2200)," \
                " (9, 'M', 1, 2200), (9, 'M', 2, 2400), (9, 'M', 3, 2800)," \
                " (10, 'F', 1, 1600), (10, 'F', 2, 1800), (10, 'F', 3, 2000)," \
                " (10, 'M', 1, 2000), (10, 'M', 2, 2400), (10, 'M', 3, 2600)," \
                " (11, 'F', 1, 1600), (11, 'F', 2, 1800), (11, 'F', 3, 2000)," \
                " (11, 'M', 1, 2000), (11, 'M', 2, 2200), (11, 'M', 3, 2600)"

    execute_query(query)

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

    fill_ageMappingTable()

    fill_diseasesTable()

    fill_intolerancesTable()

    fill_preferencesTable()

    fill_kcal_table()

if __name__ == "__main__":
    main()