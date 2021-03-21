To run the test cases, execute:

```console
$ pytest unit-tests.py --log-cli-level=DEBUG 
```

The output on the console for a successful test run will be as follows:

```console
================================================================================================================== test session starts ==================================================================================================================
platform darwin -- Python 3.9.2, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /Users/vischan2/DS
collected 9 items                                                                                                                                                                                                                                       

API-unit-tests.py::TestCases::test_200_response 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:32 TEST 1: Checking URL Lookup for Benign category
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=translate.googleusercontent.com HTTP/1.1" 200 309
INFO     API-unit-tests:API-unit-tests.py:37 {'data': {'URL category': {'translate.googleusercontent.com': 'Benign'}}, 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 200, 'message': 'INFO: The request has succeeded.'}}
PASSED                                                                                                                                                                                                                                            [ 11%]
API-unit-tests.py::TestCases::test_benign_category 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:41 TEST 1: Checking URL Lookup for Benign category
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=reddit.com HTTP/1.1" 200 288
INFO     API-unit-tests:API-unit-tests.py:46 {'data': {'URL category': {'reddit.com': 'Benign'}}, 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 200, 'message': 'INFO: The request has succeeded.'}}
PASSED                                                                                                                                                                                                                                            [ 22%]
API-unit-tests.py::TestCases::test_spyware_category 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:50 TEST 2: Checking URL Lookup for Spyware category
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=manaplas.com/bankofamerica.comr/home.php HTTP/1.1" 200 319
INFO     API-unit-tests:API-unit-tests.py:55 {'data': {'URL category': {'manaplas.com/bankofamerica.comr/home.php': 'Spyware'}}, 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 200, 'message': 'INFO: The request has succeeded.'}}
PASSED                                                                                                                                                                                                                                            [ 33%]
API-unit-tests.py::TestCases::test_malware_category 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:59 TEST 3: Checking URL Lookup for Malware category
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=recovery-notifications-issue-identity-pages.gq HTTP/1.1" 200 325
INFO     API-unit-tests:API-unit-tests.py:64 {'data': {'URL category': {'recovery-notifications-issue-identity-pages.gq': 'Malware'}}, 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 200, 'message': 'INFO: The request has succeeded.'}}
PASSED                                                                                                                                                                                                                                            [ 44%]
API-unit-tests.py::TestCases::test_adware_category 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:68 TEST 4: Checking URL Lookup for Adware category
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=verificationpayment.com/Login.php HTTP/1.1" 200 311
INFO     API-unit-tests:API-unit-tests.py:73 {'data': {'URL category': {'verificationpayment.com/Login.php': 'Adware'}}, 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 200, 'message': 'INFO: The request has succeeded.'}}
PASSED                                                                                                                                                                                                                                            [ 55%]
API-unit-tests.py::TestCases::test_phishing_category 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:77 TEST 5: Checking URL Lookup for Phishing category
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=http://mail.securelloyd-help-team.com/lloyds/Login.php HTTP/1.1" 200 334
INFO     API-unit-tests:API-unit-tests.py:82 {'data': {'URL category': {'http://mail.securelloyd-help-team.com/lloyds/Login.php': 'Phishing'}}, 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 200, 'message': 'INFO: The request has succeeded.'}}
PASSED                                                                                                                                                                                                                                            [ 66%]
API-unit-tests.py::TestCases::test_ransomware_category 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:86 TEST 6: Checking URL Lookup for Ransomware category
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=royalmail-uk-deliveries.com/billing.php HTTP/1.1" 200 321
INFO     API-unit-tests:API-unit-tests.py:91 {'data': {'URL category': {'royalmail-uk-deliveries.com/billing.php': 'Ransomware'}}, 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 200, 'message': 'INFO: The request has succeeded.'}}
PASSED                                                                                                                                                                                                                                            [ 77%]
API-unit-tests.py::TestCases::test_401_status 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:95 TEST 6: Checking if unauthorized requests are returned with 401
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /urlinfo/1?query=https://www.amazon.com HTTP/1.1" 401 272
INFO     API-unit-tests:API-unit-tests.py:102 {'data': '', 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 401, 'message': 'ERROR: Unauthorized. The provided API token is not a valid registered token.'}}
PASSED                                                                                                                                                                                                                                            [ 88%]
API-unit-tests.py::TestCases::test_404_status 
--------------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------------
INFO     API-unit-tests:API-unit-tests.py:106 TEST 6: Checking if unsupported resource requests are returned with 404
DEBUG    urllib3.connectionpool:connectionpool.py:227 Starting new HTTP connection (1): 0.0.0.0:5000
DEBUG    urllib3.connectionpool:connectionpool.py:452 http://0.0.0.0:5000 "GET /wrong-resource?query=https://www.forbes.com HTTP/1.1" 404 446
INFO     API-unit-tests:API-unit-tests.py:111 {'data': '', 'info': {'engine': {'version': '1.0'}, 'timestamp': 'Sun, 21 Mar 2021 04:46:45 GMT'}, 'response_status': {'code': 404, 'message': 'ERROR: The server does not support the functionality to fulfill this request. This could be because the requested URL was not found on the server or a valid URL was not provided. If you entered the URL manually, please re-check the URL and try again.'}}
PASSED                                                                                                                                                                                                                                            [100%]

=================================================================================================================== 9 passed in 0.51s ===================================================================================================================
```
