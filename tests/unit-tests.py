import requests, json
import logging
from dotenv import load_dotenv
import os
import pytest


@pytest.fixture
def logger_handler():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    load_dotenv('../.env')
    return logger


@pytest.fixture
def headers_dict():
    test_token = "user-token-555"
    headers_dict = {"X-Api-Key": test_token}
    return headers_dict


@pytest.fixture
def server_access():
    server_address = str(os.getenv('API_SERVER_IP')) + ":" + str(os.getenv('API_SERVER_PORT'))
    return server_address


class TestCases():

    def test_200_response(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 1: Checking URL Lookup for Benign category")
        test_url = "translate.googleusercontent.com"
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["response_status"]["code"] == 200

    def test_benign_category(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 1: Checking URL Lookup for Benign category")
        test_url = "reddit.com"
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["data"]["URL category"][test_url] == "Benign"

    def test_spyware_category(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 2: Checking URL Lookup for Spyware category")
        test_url = "manaplas.com/bankofamerica.comr/home.php"
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["data"]["URL category"][test_url] == "Spyware"

    def test_malware_category(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 3: Checking URL Lookup for Malware category")
        test_url = "recovery-notifications-issue-identity-pages.gq"
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["data"]["URL category"][test_url] == "Malware"

    def test_adware_category(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 4: Checking URL Lookup for Adware category")
        test_url = "verificationpayment.com/Login.php"
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["data"]["URL category"][test_url] == "Adware"

    def test_phishing_category(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 5: Checking URL Lookup for Phishing category")
        test_url = "http://mail.securelloyd-help-team.com/lloyds/Login.php"
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["data"]["URL category"][test_url] == "Phishing"

    def test_ransomware_category(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 6: Checking URL Lookup for Ransomware category")
        test_url = "royalmail-uk-deliveries.com/billing.php"
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["data"]["URL category"][test_url] == "Ransomware"

    def test_401_status(self, logger_handler, server_access):
        logger_handler.info("TEST 6: Checking if unauthorized requests are returned with 401")
        test_url = "https://www.amazon.com"
        test_token = "NO-TOKEN"
        headers_dict = {"X-Api-Key": test_token}
        response = requests.get("http://{}/urlinfo/1?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["response_status"]["code"] == 401

    def test_404_status(self, logger_handler, headers_dict, server_access):
        logger_handler.info("TEST 6: Checking if unsupported resource requests are returned with 404")
        test_url = "https://www.forbes.com"
        response = requests.get("http://{}/wrong-resource?query={}"
                                .format(server_access, test_url), headers=headers_dict)
        dict_response = (json.loads(response.text))
        logger_handler.info(dict_response)
        assert dict_response["response_status"]["code"] == 404
