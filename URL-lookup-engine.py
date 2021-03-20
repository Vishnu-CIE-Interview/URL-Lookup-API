#!/usr/bin/python3
from flask import Flask, request
from flask_mysqldb import MySQL
import flask_mysqldb
import hmac
import hashlib
import os
import pymysql
from datetime import datetime
import logging
import argparse
from pymemcache.client import base
from logging.handlers import SMTPHandler
from flasgger import Swagger
#Command line flag to turn on debug logging


def initialize_command_line_args():

    """
    initialize_command_line_args() initiates CLI flags, which the server operator can use to enable debug level logging or email alerting of errors
    :return: the flags used to activate or disable the debug logging and email alerting
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="API lookup service to detect maliciousness of URLs")
    parser.add_argument('--debug', dest='DEBUG_FLAG', required=False,
                        help='Flag to turn on debug level logging when needed. Accepted values are 1 or 0.', default='0', choices=['0', '1'])
    parser.add_argument('--email_alerts', dest='EMAIL_ALERT_FLAG', required=False,
                        help='Flag to turn on email alerts to notify critical server errors that need immediate action. Accepted values are 1 or 0.', default='0', choices=['0', '1'])

    args, unknown = parser.parse_known_args()

    DEBUG_FLAG = args.DEBUG_FLAG
    EMAIL_ALERT_FLAG = args.EMAIL_ALERT_FLAG

    return [DEBUG_FLAG, EMAIL_ALERT_FLAG]

def debug_and_email_alert_enabler(cli_flags,app):
    """
    debug_and_email_alert_enabler() instantiates the logging feature at appropriate levels
    :return: None
    """
    #enable debug level logging if applicable
    DEBUG_FLAG = cli_flags[0]
    if {'0': False, '1': True}[DEBUG_FLAG]:
        app.logger.setLevel(logging.DEBUG)


    #add alert mail handling if applicable
    EMAIL_FLAG = cli_flags[1]
    if {'0': False, '1': True}[EMAIL_FLAG]:
        app.logger.addHandler(alert_critical_errors_on_email())


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


def initialize_memcached_caching():
    """
    initialize_memcached_caching() will initialize a memcached client that will communicate with the memcached server that maintains a data cache
    :return: the initialized memcached client
    """
    memcached_client = base.Client(('localhost', 12345))
    return memcached_client

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


def alert_critical_errors_on_email():
    """
    alert_critical_errors_on_email() will initialize a mail handler to be used for email alerting
    :return: the initialized mail handler set to contain critical error logs
    """

    mail_handler = SMTPHandler(
        mailhost=('127.0.0.1',25),
        fromaddr='API-error-monitoring@cisco.com',
        toaddrs=['vischan2@cisco.com'],
        subject='ATTENTION : Critical Application Error - Action Needed!'
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))

    return mail_handler


def app_function():

    app = Flask(__name__)
    mysql = MySQL(app)
    swagger = Swagger(app)
    app.logger.setLevel(logging.INFO)

    cli_flags = initialize_command_line_args()
    debug_and_email_alert_enabler(cli_flags,app)


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

        """ endpoint that returns the URL lookup categorization
        The service provides URL lookup that categorizes input URLs based on level of maliciousness.
        ---
        info:
          title: URL Lookup API
          description: The service provides URL lookup that categorizes input URLs based on level of maliciousness.
          version: 1.0.0
        basePath: /v1
        get:
          summary: Returns URL Lookup response
          description: The resource accepts an URL as a query parameter, and returns the category in the response payload.
          produces:
            - application/json
        parameters:
            -   in: query
                name: query
                type: string
                description: The URL that the user provides for lookup.
                required: true
            -   in: header
                name: X-Api-Key
                type: string
                description: The user token used for authentication to access the API service.
                required: true
        responses:
            200:
                description: URL Lookup request was successfully processes and responded.
            401:
                description: User provided API-token could not be authenticated.
            404:
                description: The server does not support the requested resource functionality to fulfill this request.
            500:
                description: The request could not be processed at this moment due to an Internal Server Error.
        schema:
            type: object
   """

        headers = request.headers
        auth_token = headers.get("X-Api-Key") #expect an auth token assigned to user as "user-token-555"
        url = request.args.get('query') #fetch url passed as an API query

        user_sha_signature = create_sha_signature(auth_token)
        if verify_sha_signature_in_datastore(user_sha_signature):
            app.logger.info("User provided API token successfully authenticated, valid response will be send")


            #Attempt to get from cache first, only then go to DB

            memcached_client = initialize_memcached_caching()
            cached_result = memcached_client.get(url)

            if cached_result:
                app.logger.info("cached values found in memcached")
                url_category = cached_result.decode('utf-8')
            else:
                app.logger.info("cached values not available, will query the database")
                db_cursor = mysql.connection.cursor()
                db_cursor.execute("select reputation from local_url_lookup where url='{}';".format(url))
                query_fetch = db_cursor.fetchall()
                if query_fetch:
                    url_category = query_fetch()[0][0]
                    memcached_client.set(url, url_category,  expire=600)
                else:
                    url_category="" #uncategorized URL in the local datastore


            if len(url_category): #categorization exists
                status_code = 200
                return response_builder({"URL category": {url: url_category}}, status_code, "INFO: The request has succeeded."), status_code
            else: #categorization does not exist
                status_code = 200
                return response_builder( {"URL category": {url: 'Uncategorized'}}, status_code, "INFO: The request has succeeded."), status_code


        else:
            app.logger.info("User provided API token could not be authenticated with the stored hash on datastore")
            status_code = 401
            return response_builder("",status_code,"ERROR: Unauthorized. The provided API token is not a valid registered token."), status_code

    @app.route('/<path:path>')
    @app.route('/', defaults={'path': None})
    def unsupported_resource(path):
        status_code = 404
        return response_builder("", status_code,
                                "ERROR: The server does not support the functionality defined by [{}], to fulfill this request. "
                                "This could be because the requested URL was not found on the server or a valid URL was not provided. "
                                "If you entered the URL manually, please re-check the URL and try again.".format(path)), status_code

    return app

if __name__ == '__main__':
    app_function().run(host='0.0.0.0', port=5003, debug=True)