#!/usr/bin/python3
from flask import Flask, request
from flask_mysqldb import MySQL
import flask_mysqldb
import hmac
import hashlib
import os
import pymysql
from datetime import datetime


def create_sha_signature(access_token):
    """
    create_sha_signature() computes a cryptographic HMAC signature in order to authenticate API requests
    :param access_token: this value is retrieved from the authentication header of incoming requests
    :return: the computed HMAC signature in string type is returned
    """

    api_key = os.getenv('API_KEY') #server env variable
    print(api_key)
    print(access_token)
    digest = hmac.new(bytes(api_key, 'UTF-8'), bytes(access_token, 'UTF-8'), hashlib.sha256)
    signature = digest.hexdigest()
    return signature


def verify_sha_signature_in_datastore(computed_hash):
    """
    verify_sha_signature_datastore() verifies if the computed hash matches with a recognized has on the datastore.
    :param computed_hash: this value is the computed hash using the HMAC algorithm
    :return: boolean decision whether the hash can be used to allow authentication OR denied
    """
    connection_object = pymysql.connect(host='localhost', user=str(os.getenv('MYSQL_USER')), password=str(os.getenv('MYSQL_PASSWORD')), db='urlengine', charset="utf8mb4",
                                       cursorclass=pymysql.cursors.DictCursor)

    cursor_object = connection_object.cursor()
    #obtain stored hash from local datastore
    hash_query = "select hash_value from local_api_hash where hash_value='{}'".format(computed_hash)
    cursor_object.execute(hash_query)
    hash_fetch = cursor_object.fetchall()
    #check if hash exists
    if len(hash_fetch):
        return True
    return False

def response_builder(data,code,status_message):
    """
    response_builder() generates the API response payload that is returned to the client
    :param data: object containing the data fields (URL Lookup information) for the API response
    :param code: the HTTP status code for the API response
    :param status_message: contains descriptive message of success or failure returned to the client
    :return: the generated response payload
    """
    response = {
        "data": data,
        "response_status": {
            "code": code,
            "message": status_message
        },
        "info": {
            "engine": {
                "version": "1.0",
            },
            "timestamp": datetime.now()
        }
    }
    return response

def app_function():

    app = Flask(__name__)
    mysql = MySQL(app)

    #to_do: store these as env variables
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_DB'] = 'urlengine'
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')


    @app.errorhandler(Exception)
    def server_error(server_internal_error):
        app.logger.exception(server_internal_error)
        return response_builder("", 500,"ERROR: The request could not be processed at this moment due to an Internal Server Error."), 500


    @app.route('/urlinfo')
    def urlinfo():

        #try:
        headers = request.headers
        auth_token = headers.get("X-Api-Key") #expect am auth token assigned to user as "user-token-555"
        url = request.args.get('query') #fetch url passed as an API query

        user_sha_signature = create_sha_signature(auth_token)
        if verify_sha_signature_in_datastore(user_sha_signature):

            db_cursor = mysql.connection.cursor()
            db_cursor.execute("select reputation from local_url_lookup where url='{}';".format(url))
            url_category = db_cursor.fetchall()

            print(url_category)
            if len(url_category):
                return response_builder({"URL category": {url: url_category[0][0]}}, 200, "INFO: The request has succeeded."), 200
            else:
                #CLOUD LOOKUP BEFORE GENERAL CONDITON, SAVE IT TO LOCAL DB
                return response_builder( {"URL category": {url: 'Uncategorized'}}, 200, "INFO: The request has succeeded."), 200


        else:

            return response_builder("",401,"ERROR: Unauthorized. The provided API token is not a valid registered token."), 401

    @app.route('/<path:path>')
    @app.route('/', defaults={'path': None})
    def unsupported_resource(path):
        return response_builder("", 501,
                                "ERROR: The server does not support the functionality [{}] to fulfill this request. "
                                "This could be because the requested URL was not found on the server or a valid URL was not provided. "
                                "If you entered the URL manually, please re-check the URL and try again.".format(path)), 501

    return app

if __name__ == '__main__':
    app_function().run(host='0.0.0.0', port=5001, debug=True)