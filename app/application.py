from flask import Flask, request, redirect, url_for
from flask_mysqldb import MySQL
from flasgger import Swagger
from dotenv import load_dotenv
from helpers import *


def app_function():
    """
    app_function() initiates the application framework to run the API services. This includes:
    -template specification
    -route definition
    -response generation
    :return: the defined application object
    """
    load_dotenv('.env')
    app = Flask(__name__)
    mysql = MySQL(app)

    # the template is used to initialize API Spec documentation and populate
    # information that is accessible at http://<api-server-ip>:port/apidocs

    template = {
        "swagger": "2.0",
        "info": {
            "title": "URL Lookup API service",
            "description": "The service provides URL lookup that categorizes input URLs based on level of maliciousness.",
            "contact": {
                "Developer": "Vishnu C",
                "email": "vischan2@cisco.com"
            },
            "version": "1.0"
        },
        "basePath": "/urlinfo?query=<url>",
        "schemes": [
            "http"
        ]
    }

    swagger = Swagger(app, template=template)

    app.logger.setLevel(logging.INFO)
    logging.basicConfig(filename='URL-api-engine.log', level=logging.DEBUG,
                        format=' %(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s')

    cli_flags = initialize_command_line_args()
    debug_and_email_alert_enabler(cli_flags, app)

    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')

    @app.errorhandler(Exception)
    def server_error(server_internal_error):
        app.logger.exception(server_internal_error)
        return response_builder("", 500,
                                "ERROR: The request could not be processed at this moment due to an Internal Server Error."), 500

    @app.route('/urlinfo/1')
    def urlinfo_v1():

        """Route endpoint that returns the URL lookup categorization
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
        auth_token = headers.get("X-Api-Key")  # expect an auth token that is registered and assigned to user
        pre_canonicalized_url = request.args.get('query')  # fetch url passed as an API query
        url = canonicalize_urls(pre_canonicalized_url)
        user_sha_signature = create_sha_signature(auth_token)
        if verify_sha_signature_in_datastore(user_sha_signature):
            app.logger.error("User provided API token successfully authenticated, valid response will be send")

            # Attempt to get from cache first, only then go to DB

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
                    url_category = query_fetch[0][0]
                    memcached_client.set(url, url_category, expire=600)
                else:
                    url_category = ""  # uncategorized URL in the local datastore

            if len(url_category):  # categorization exists
                status_code = 200
                return response_builder({"URL category": {pre_canonicalized_url: url_category}}, status_code,
                                        "INFO: The request has succeeded."), status_code
            else:  # categorization does not exist
                status_code = 200
                return response_builder({"URL category": {pre_canonicalized_url: 'Uncategorized'}}, status_code,
                                        "INFO: The request has succeeded."), status_code

        else:
            app.logger.info("User provided API token could not be authenticated with the stored hash on datastore")
            status_code = 401
            return response_builder("", status_code,
                                    "ERROR: Unauthorized. The provided API token is not a valid registered token."), status_code



    @app.route('/urlinfo/2')
    def urlinfo_v2():
        '''
        Placeholder route for version 2 of the API. Currently, this resource is not published.
        '''
        return redirect(url_for('unsupported_resource'))


    @app.route('/<path:path>')
    @app.route('/', defaults={'path': None})
    def unsupported_resource(path):
        status_code = 404
        return response_builder("", status_code,
                                "ERROR: The server does not support the functionality to fulfill this request. "
                                "This could be because the requested URL was not found on the server or a valid URL was not provided. "
                                "If you entered the URL manually, please re-check the URL and try again."), status_code

    return app
