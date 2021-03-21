import hmac
import hashlib
import os
import argparse
from dotenv import load_dotenv
import pymysql


def initialize_mysql():
    """
    initialize_mysql() initializes the mysql connection object
    :return: mysql connection object
    """
    load_dotenv('../.env')
    connection_object = pymysql.connect(host='localhost', user=str(os.getenv('MYSQL_USER')),
                                        password=str(os.getenv('MYSQL_PASSWORD')), db='urlengine', charset="utf8mb4",
                                        cursorclass=pymysql.cursors.DictCursor)

    return connection_object


def initialize_registration_command_line_args():
    """
    initialize_registration_command_line_args() accepts the authentication token for registration or unregistration.
    :return: list type containing registration or unregistration tokens for subsequent action
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Register or unregister an authentication token for the client.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--register', dest='REGISTER',
                       help='register the provided authentication token')
    group.add_argument('--unregister', dest='UNREGISTER',
                       help='unregister a known authentication token from the recognized list of tokens in the database')

    args, unknown = parser.parse_known_args()

    REGISTER = args.REGISTER
    UNREGISTER = args.UNREGISTER

    return [REGISTER, UNREGISTER]


def create_sha_signature(auth_token):
    """
    create_sha_signature() computes a cryptographic HMAC signature in order to authenticate API requests
    :param auth_token: the auth token to authenticate incoming API requests
    :return: the computed HMAC signature in string type is returned
    """
    api_key = os.getenv('API_KEY')
    digest = hmac.new(bytes(api_key, 'UTF-8'), bytes(auth_token, 'UTF-8'), hashlib.sha256)
    signature = digest.hexdigest()
    return signature


def validate_if_token_exists(auth_token):
    """
    validate_if_token_exists() checks the database if the computed hash of the auth token is already registered
    :param auth_token: the auth token to authenticate incoming API requests
    :return: returns Boolean
    """
    try:
        connection_object = initialize_mysql()
        computed_hash = create_sha_signature(auth_token)

        hash_query = "select hash_value from local_api_hash where hash_value='{}'".format(computed_hash)
        cursor_object = connection_object.cursor()
        cursor_object.execute(hash_query)
        hash_fetch = cursor_object.fetchall()

        if len(hash_fetch):
            return True
        return False
    except Exception as error:
        raise Exception("Validation of auth token in the database has failed - {}".format(error))


def register_token(auth_token):
    """
    register_token() registers the provided authentication token after computing HMAC signature and then inserting it into database
    :param auth_token: the auth token to authenticate incoming API requests
    :return: None
    """
    try:
        connection_object = initialize_mysql()
        if not validate_if_token_exists(auth_token):
            computed_hash = create_sha_signature(auth_token)
            hash_insert = "insert into local_api_hash (hash_value) values ('{}');".format(computed_hash)
            cursor_object = connection_object.cursor()
            cursor_object.execute(hash_insert)
            connection_object.commit()
            print(
                "Token is now successfully registered with the server. To authenticate REST API requests, provide the registered token as 'X-Api-key' in the HTTP header.")
        else:
            print("This is an already registered token! No action needed.")
    except Exception as error:
        raise Exception("Inserting computed hash into the database has failed - {}".format(error))


def unregister_token(auth_token):
    """
    unregister_token() unregisters the provided authentication token, by computing HMAC signature and removing its occurrence from the database
    :param auth_token: the auth token to authenticate incoming API requests
    :return: None
    """
    try:
        connection_object = initialize_mysql()
        if validate_if_token_exists(auth_token):
            computed_hash = create_sha_signature(auth_token)
            hash_delete = "delete from local_api_hash where hash_value='{}';".format(computed_hash)
            cursor_object = connection_object.cursor()
            cursor_object.execute(hash_delete)
            connection_object.commit()
            print(
                "Token is now successfully unregistered. This token cannot be used for authenticating API requests with the server anymore.")
        else:
            print("This is not a registered token! No action needed.")

    except Exception as error:
        raise Exception("Deleting computed hash from the database has failed - {}".format(error))


cli_flags = initialize_registration_command_line_args()

for cli_argument in cli_flags:
    if cli_argument is not None:
        auth_token = cli_argument

if cli_flags[0] is not None:
    # flag for registratopm
    auth_token = cli_flags[0]
    print("Registering token: {}".format(auth_token))
    register_token(auth_token)

else:
    # flag for unregistration
    auth_token = cli_flags[1]
    print("Ungistering token: {}".format(auth_token))
    unregister_token(auth_token)
