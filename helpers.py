import hmac
import hashlib
import os
import pymysql
from datetime import datetime
import logging
import argparse
from pymemcache.client import base
from logging.handlers import SMTPHandler


def initialize_command_line_args():
    """
    initialize_command_line_args() initiates CLI flags, which the server operator can use to enable debug level logging or email alerting of errors
    :return: the flags used to activate or disable the debug logging and email alerting
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="API lookup service to detect maliciousness of URLs")
    parser.add_argument('--debug', dest='DEBUG_FLAG', required=False,
                        help='Flag to turn on debug level logging when needed. Accepted values are 1 or 0.',
                        default='0', choices=['0', '1'])
    parser.add_argument('--email_alerts', dest='EMAIL_ALERT_FLAG', required=False,
                        help='Flag to turn on email alerts to notify critical server errors that need immediate action. Accepted values are 1 or 0.',
                        default='0', choices=['0', '1'])

    args, unknown = parser.parse_known_args()

    DEBUG_FLAG = args.DEBUG_FLAG
    EMAIL_ALERT_FLAG = args.EMAIL_ALERT_FLAG

    return [DEBUG_FLAG, EMAIL_ALERT_FLAG]


def debug_and_email_alert_enabler(cli_flags, app):
    """
    debug_and_email_alert_enabler() instantiates the logging feature at appropriate levels
    :return: None
    """
    # enable debug level logging if applicable
    DEBUG_FLAG = cli_flags[0]
    if {'0': False, '1': True}[DEBUG_FLAG]:
        app.logger.setLevel(logging.DEBUG)

    # add alert mail handling if applicable
    EMAIL_FLAG = cli_flags[1]
    if {'0': False, '1': True}[EMAIL_FLAG]:
        app.logger.addHandler(alert_critical_errors_on_email())

    return None


def create_sha_signature(access_token):
    """
    create_sha_signature() computes a cryptographic HMAC signature in order to authenticate API requests
    :param access_token: this value is retrieved from the authentication header of incoming requests
    :return: the computed HMAC signature in string type is returned
    """

    api_key = os.getenv('API_KEY')
    digest = hmac.new(bytes(api_key, 'UTF-8'), bytes(access_token, 'UTF-8'), hashlib.sha256)
    signature = digest.hexdigest()
    return signature


def verify_sha_signature_in_datastore(computed_hash):
    """
    verify_sha_signature_datastore() verifies if the computed hash matches with a recognized has on the datastore.
    :param computed_hash: this value is the computed hash using the HMAC algorithm
    :return: boolean decision whether the hash can be used to allow authentication OR denied
    """
    connection_object = pymysql.connect(host='localhost', user=str(os.getenv('MYSQL_USER')),
                                        password=str(os.getenv('MYSQL_PASSWORD')), db='urlengine', charset="utf8mb4",
                                        cursorclass=pymysql.cursors.DictCursor)

    cursor_object = connection_object.cursor()
    # obtain stored hash from local datastore
    hash_query = "select hash_value from local_api_hash where hash_value='{}'".format(computed_hash)
    cursor_object.execute(hash_query)
    hash_fetch = cursor_object.fetchall()
    # check if hash exists
    if len(hash_fetch):
        return True
    return False


def initialize_memcached_caching():
    """
    initialize_memcached_caching() will initialize a memcached client that will communicate with the memcached server that maintains a data cache
    :return: the initialized memcached client
    """
    memcached_client = base.Client((os.getenv('MEMCACHED_SERVER'), int(os.getenv('MEMCACHED_PORT'))))
    return memcached_client


def response_builder(data, code, status_message):
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
        mailhost=(os.getenv('SMTP_MAIL_SERVER'), int(os.getenv('SMTP_MAIL_PORT'))),
        fromaddr=os.getenv('SMTP_FROM_ADDRESS'),
        toaddrs=[os.getenv('SMTP_TO_ADDRESS')],
        subject='ATTENTION : Critical Application Error - Action Needed!'
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))

    return mail_handler


def canonicalize_urls(url):
    """
    canonicalize_urls() will standardize URLs in the format for comparison across the database
    :param url: the raw input url before canonicalization
    :return: the canonicalized url string is returned
    """
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    url = "".join(url.split())
    if url.startswith("www."):
        url = url.replace("www.", "")
    if url.endswith("/"):
        url = url[:-1]
    if url.find('/') != -1:
        domain_split = url.find('/')
        url = url[:domain_split].lower() + url[domain_split:]
    else:
        url = url.lower()
    return url
