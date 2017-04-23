import sqlite3 as sql
from passlib.hash import pbkdf2_sha256
from datetime import date, timedelta, datetime
from dateutil import parser

class DatabaseHandler:

    def __init__(self, dbName):
        self._dbName = dbName

    def _encrypt_pass(self, password):
        """

        :param password:        the password to encrypt
        :return:                the encrypted password
        """
        hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        return hash

    def _check_pass(self, password, hash):
        """

        :param password:        the password to be tested
        :param hash:            the hashed password
        :return:                True - if the passwords match
                                False - otherwise
        """
        return pbkdf2_sha256.verify(password, hash)

    def _execute_INSERT(self, table, cols, *args):
        """

        :param table:       the table to insert into
        :param cols:        the list of columns we want to insert to
        :param items:       the list of items we want to insert
        :return:            -
        """

        query = "INSERT INTO " + table + " ("

        qmarks = "("

        for col in cols:
            qmarks = qmarks + "?"
            query += col
            if col != cols[-1]:
                query += ", "
                qmarks += ", "
            else:
                query += ") "
                qmarks += ") "

        query += "VALUES " + qmarks
        print(query)

        self._execute_query(query, *args)

    def _execute_SELECT(self, table, conds, cols=["*"], limit=None, order=None, groupBy=None):
        """
                    function that executes a SELECT query
        :param cols:        the list of columns we want. default ['*']
        :param table:       the table name
        :param conds:       the conditions, as a string
        :param limit:       how many results to return. default None
        :param order:       the way to order the results. default None
        :param groupBy:     the way to group the results. default None
        :return:            the list representing the results of the query
        """

        cols_string = ",".join(cols)
        query = "SELECT " + cols_string + " FROM " + str(table)

        if conds != None:
            query += " WHERE " + str(conds)

        if order != None:
            query += " ORDER BY " + str(order)

        if groupBy != None:
            query += " GROUP BY " + str(groupBy)

        if limit != None:
            query += " LIMIT " + str(limit)

        print(query)

        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        results = list(set(cur.fetchall()))
        con.commit()
        con.close()

        return results

    def _execute_query(self, query, *args):
        """
            Function that executes a given query, except SELECT queries
        :param query:       the query to be executed
        :param args:        the arguments to be inserted
        :return:
        """

        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query, args)
        con.commit()
        con.close()

    def try_to_login_user(self, email, password):
        """
            Function that tries to authenticate a given user
        :param email:           the email of the user
        :param password:        the password
        :return:                a (Bool, Int) tuple of the format
                            <success_status, userID>
        """
        result = self._execute_SELECT(
            table='credentials',
            conds='email= "' + email + '"',
            cols=['userID', 'pass']
        )

        if len(result) != 1:
            #email not valid or duplicated email
            return False, -1, None
        else:
            #email valid, now check the password
            success = self._check_pass(password, result[0][1])
            if success:
                uid = result[0][0]
                result = self._execute_SELECT(
                    table='userData',
                    conds='id='+str(uid),
                    cols=['name']
                )
                return success, uid, result[0][0]
            else:
                return False, -1, None

    def signup_step_one(self, email, password, name):
        """
            Method that adds a new user to the database
        :param email:           the email of the user
        :param password:        the password of the user
        :param name:            the name of the user
        :return:                <userID, True> if it succeeded
                                <-1, False> otherwise
        """

        #First, make sure the same data does not exist in the database already
        result = self._execute_SELECT(
            table='credentials',
            conds='email="' + str(email) + '"',
        )
        if len(result) != 0:
            #user already in the db
            return -1, False

        #Now, create the user in userData
        self._execute_INSERT('userData', ['name'], str(name))

        #Now, let's get its ID
        user_id= self._execute_SELECT(
            table='userData',
            conds='name="' + str(name)+'"',
            cols=['MAX(id) AS id']
        )

        #Now, create the entry in credentials
        self._execute_INSERT(
            'credentials',
            ['email', 'pass', 'userID'],
            email, self._encrypt_pass(password), user_id[0][0]
        )

        return user_id[0][0], True

    def signup_step_two(self, userID, date_of_birth, gender, activity_level, target):
        """

        :param userID:                  The ID of the user we want to update
        :param date_of_birth:           The date of birth of the user
                                        Has to be a string of the format:
                                             %Y-%m-%d
        :param gender:                  The gender of the user
        :param activity_level:          The activity level of the user
        :param target:                  The target of the user (ex: losing weight, gaining weight, etc)
        :return:                        True, if successful
                                        False, otherwise
        """
        query = "UPDATE userData " \
                "SET date_of_birth= '" + str("1996-02-20") + "', " \
                    "gender='" + str(gender) + "', " \
                    "activity_level=" + str(activity_level) + ", " \
                    "target='" + str(target) + \
                "' WHERE id=" + str(userID)

        self._execute_query(query)

        return True

    def add_intolerances(self, userID, intolerances):
        """

        :param userID:              The id we want to run this for
        :param intolerances:        The list of intolerances we have
        :return:                    -
        """

        for intolerance in intolerances:
            intolerance_id = self._execute_SELECT(
                table='intolerances',
                conds='name="' + str(intolerance) + '"',
                cols=['id'],
                limit=1
            )

            if len(intolerance_id) > 0:

                intolerance_id = intolerance_id[0][0]

                self._execute_INSERT(
                    'userIntolerances',
                    ['intolID', 'userID'],
                    str(intolerance_id), str(userID)
                )

    def add_diseases(self, userID, diseases):
        """

        :param userID:              The id of the user we run this for
        :param diseases:            The list of diseases
        :return:                    -
        """

        for disease in diseases:
            disease_id = self._execute_SELECT(
                table='diseases',
                conds='name="' + str(disease)+'"',
                cols=['id'],
                limit=1
            )

            if len(disease_id) > 0:
                disease_id = disease_id[0][0]
                self._execute_INSERT(
                    'userDiseases',
                    ['diseaseID', 'userID'],
                    disease_id, userID
                )

    def add_preferences(self, userID, preferences):
        for preference in preferences:
            preference_id = self._execute_SELECT(
                table='preferences',
                conds='name="' + str(preference) + '"',
                cols=['id'],
                limit=1
            )

            if len(preference_id) > 0:
                preference_id = preference_id[0][0]
                self._execute_INSERT(
                    'userPreferences',
                    ['prefID', 'userID'],
                    preference_id, userID
                )

    def get_intolerances(self, userID):
        """

        :param userID:      the id of the user
        :return:            a list of his/ hers intolerances
        """

        query = "SELECT i.name FROM userIntolerances AS ui " \
                "JOIN intolerances AS i ON ui.intolID=i.id " \
                "WHERE ui.userID="+str(userID)

        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        results = list(set(cur.fetchall()))
        con.commit()
        con.close()

        intolerances_list = list()

        for result in results:
            intolerances_list.append(result[0])

        return intolerances_list

    def get_preferences(self, userID):
        """

            :param userID:      the id of the user
            :return:            a list of his/ hers preferences
        """

        query = "SELECT p.name FROM userPreferences AS up " \
                "JOIN preferences AS p ON up.prefID=p.id " \
                "WHERE up.userID=" + str(userID)

        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        results = list(set(cur.fetchall()))
        con.commit()
        con.close()

        preferences_list = list()

        for result in results:
            preferences_list.append(result[0])

        return preferences_list

    def get_diseases(self, userID):
        """

        :param userID:          The id of the user we want to generate these for
        :return:                a list of his/ hers diseases
        """

        query = "SELECT d.name FROM userDiseases AS ud " \
                "JOIN diseases AS d ON ud.disID=d.id " \
                "WHERE ud.userID=" + str(userID)

        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        results = list(set(cur.fetchall()))
        con.commit()
        con.close()

        diseases_list = list()

        for result in results:
            diseases_list.append(result[0])

        return diseases_list

    def get_kcal_per_day(self, userID):
        """

        :param userID:          The id of the user
        :return:                The recommended number of calories for a day
        """

        result = self._execute_SELECT(
            table='userData',
            conds='id='+str(userID),
            cols=['gender', 'date_of_birth', 'activity_level', 'target']
        )

        gender = result[0][0]
        birth_date = result[0][1]
        try:
            dt = parser.parse(birth_date)
            age = (datetime.today() - dt) // timedelta(days=365.2425)
        except:
            age = 21
        level = result[0][2]
        target = result[0][3]

        query = "SELECT kcal.kcal " \
                "FROM (" \
                    "SELECT id " \
                    "FROM ageMapping AS am " \
                    "WHERE left_ageLimit<="+ str(age)+ " " \
                                "AND right_ageLimit>="+str(age) + \
                    ") AS age_group "  \
                "JOIN kcal ON kcal.age_group = age_group.id " \
                    " AND kcal.gender='" + str(gender[0]) + "'"\
                    " AND kcal.level=" + str(level)

        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        results = list(set(cur.fetchall()))
        con.commit()
        con.close()

        recommend = results[0][0]

        if target == 'lose':
            return recommend - 200
        elif target == 'gain':
            return recommend + 200
        else:
            return recommend

    def add_to_history(self, userID, recipeID):
        """

        :param userID:          the id of the user
        :param recipeID:        the id of the recipe
        :return:                -
        """

        date = datetime.today()

        self._execute_INSERT(
            'userHistory',
            ['userID', 'recipe_ID', 'date'],
            userID, recipeID, date
        )

    def get_history(self, userID):
        """

        :param userID:      The id of the user
        :return:            The last 5 recipes used by this user, as ids
        """
        results = self._execute_SELECT(
            table='userHistory',
            conds='userID='+str(userID),
            cols=["recipe_id"],
            order="date DESC",
            limit=5
        )

        history = list()

        for result in results:
            history.append(result[0])

        return history