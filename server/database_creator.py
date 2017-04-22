import sqlite3 as sql

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
                " userName VARCHAR(50), " \
                " pass VARCHAR(32)" \
             ")"
    execute_query(query)


def main():
    #(1) Creating credentials table
    create_credentials_table()

if __name__ == "__main__":
    main()