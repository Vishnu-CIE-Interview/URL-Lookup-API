#!/usr/bin/python3
from flask import Flask, request
from flask_mysqldb import MySQL
import flask_mysqldb

def app_function():
    app = Flask(__name__)
    mysql = MySQL(app)


    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'admin123'
    app.config['MYSQL_DB'] = 'urlengine'


    @app.route('/')
    def index():
        return 'Index Page'


    def get_hashed_api_key():
        try:
            db_cursor = mysql.connection.cursor()
            db_cursor.execute("select reputation from local_url_lookup where url='{}';".format(url))
            url_category = db_cursor.fetchall()

            print(url_category)
            if len(url_category):
                return {url: url_category[0][0]}
            else:
                # CLOUD LOOKUP BEFORE GENERAL CONDITON, SAVE IT TO LOCAL DB
                return {url: 'Uncategorized'}


        except Exception as e:
            print('Database access failed!')


    @app.route('/urlinfo')
    def urlinfo():

        headers = request.headers
        auth = headers.get("X-Api-Key")
        url = request.args.get('query')

        if auth == 'hashthisauthcodeindb':

            try:
                db_cursor = mysql.connection.cursor()
                db_cursor.execute("select reputation from local_url_lookup where url='{}';".format(url))
                url_category = db_cursor.fetchall()

                print(url_category)
                if len(url_category):
                    return {url: url_category[0][0]}
                else:
                    #CLOUD LOOKUP BEFORE GENERAL CONDITON, SAVE IT TO LOCAL DB
                    return {url: 'Uncategorized'}


            except Exception as e:
                print('Database access failed!')

        else:
            return {"message": "ERROR: Unauthorized"}, 401



    @app.route('/user/<string:username>')
    def show_user_profile(username):
        # show the user profile for that user
        return 'User is {}'.format(username)

    return app


if __name__ == '__main__':
    app_function().run(host='0.0.0.0', port=5000, debug=True)
