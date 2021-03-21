# URL-Lookup-API
The API provides URL lookup service that categorizes input URLs based on level of maliciousness.
<img width="1261" alt="API-service-diagram" src="https://user-images.githubusercontent.com/81005592/111884218-6a2a3380-897d-11eb-94cc-873a0d2f8468.png">

## Project title


## Motivation


## Screenshots


## Technology and frameworks used

<b>Built with:</b>
1. Flask API Framework: parallelprojects.com/p/flask
2. Memcached Distributed Caching System: memcached.org
3. MySQL Database Service: dev.mysql.com

## Features



## Installation

The main server listening to API requests is where the Flask application running on Python 3.9.2 is deployed. This can be a Debian/Ubuntu, CentOS or any Linux based system. 

The application directory consists of three files:

1. URL-lookup-engine.py 
2. requirements.txt
3. .env 

The first step is to install the dependencies:

```console
$sudo pip3 install -r requirements.txt
```

After the dependencies are installed, we need to configure the environmental variables from .env file. 

The .env file contains the user configurable variables that the main API service will auto-configure for providing access to caching, database service and email-alerting. 

Before deploying the server into production, change the following environmental variables listed in this file.

The initial values listed here are only placeholder entries.

The server key, credentials or IP addresses should NOT be exposed outside of the production server.

Contents of .env file that needs to be configured by the user:
```shell
API_KEY=serverspecial
MYSQL_HOST=127.0.0.1
MYSQL_DB=urlengine
MYSQL_USER=root
MYSQL_PASSWORD=admin123
MEMCACHED_SERVER=127.0.0.1
MEMCACHED_PORT=12345
SNMP_MAIL_SERVER=127.0.0.1
SNMP_MAIL_PORT=25
SNMP_FROM_ADDRESS=API-error-monitoring@URLService.com
SNMP_TO_ADDRESS=administrator@company.com
```

Once this initial configuration is complete, the following servers need to be set up before the main service can be initiated. 

### Memcached Server

The Memcached server should be accessible and routable to the network where the API production server is deployed. If the server chosen is a Debian/Ubuntu machine, the Memcached service can be installed on it using the command:

```console
$sudo apt-get install memcached
```
Once installed, the caching end point can be initialized as follows by providing the port number. Once initialized, the caching layer will be connected to using the server’s IP and port address. This combination should be provided in the .env file as described earlier.

```console
$sudo memcached -p 12345
```

### Database server

The MySQL database contains the URL categorization based on malware types. The schema for the database is available in the file mysql_database_schema.sql. The database server should be accessible and routable to the main API server. MySQL service should be installed on the Linux machine. If the server is Debian/Ubuntu based, MySQL service can be installed as follows:

```console
$sudo apt-get install mysql-server
$sudo mysql_secure_installation
$sudo systemctl enable mysql
$sudo mysql -u root -p
$mysql>
```
Create the database and tables necessary for the API service as follows by sourcing the schema file as follows:

```console
mysql> source mysql_database_schema.sql
```

### SMTP Email Alerting Server

The SMTP server is used as a forwarding point to send out production critical errors and alerts from the API service, which demand immediate administrator and/or developer attention. Ensure that this server is reachable on the network with the main API server. If a Debian/Ubuntu machine is used for this purpose, a console level notification system can be initialized using Python as follows. Once this is set up, the API service will reach out to this mailing server with any urgent and critical failures, with a log snippet of the stacktrace and crash details.

```console
$sudo python -m smtpd -n -c DebuggingServer 127.0.0.1:25 
```

We are now ready to deploy the API server into production.  


## Deployment

The supported command line arguments can be checked as follows:
```
$ python3 URL-lookup-engine.py -h
usage: URL-lookup-engine.py [-h] [--debug {0,1}] [--email_alerts {0,1}]

API lookup service to detect maliciousness of URLs

optional arguments:
  -h, --help            show this help message and exit
  --debug {0,1}         Flag to turn on debug level logging when needed. Accepted values are 1 or 0. (default: 0)
  --email_alerts {0,1}  Flag to turn on email alerts to notify critical server errors that need immediate action. Accepted values are 1 or 0. (default: 0)
```

In order to deploy the service:
```console
$ python3 URL-lookup-engine.py --debug 0 --email_alerts 1
```
The service is now listening on the IP address and port specified in the .env configuration file. 


## How to use the service?

URL Lookup API service is an **authentication based service**. Hence, in order to establish a REST API communication with the server, the user needs to provide an user-token which is registered with the server. This token will be passed in the HTTP Header as an **X-API-Key**. The "query" parameter will be used to provide the URL that the client wishes to lookup through the service. 

A sample client side cURL request and response from the API server will be as follows:

```console
$ curl -X GET "http://0.0.0.0:5000/urlinfo?query=http://www.amazon.com" -H "accept: application/json" -H "X-Api-Key: user-token-555"
```

Here, the URL 'http://www.amazon.com' is provided as a query parameter for lookup, and the token used for authentication is 'user-token-555', which is pre-registered with the server.

The response payload to this request will be as follows, along with a 200 status code. The URL is classified as **Benign**.
```shell
{
  "data": {
    "URL category": {
      "http://www.amazon.com": "Benign"
    }
  }, 
  "info": {
    "engine": {
      "version": "1.0"
    }, 
    "timestamp": "Sat, 20 Mar 2021 17:11:30 GMT"
  }, 
  "response_status": {
    "code": 200, 
    "message": "INFO: The request has succeeded."
  }
}
```

Similarly, here is another URL lookup request:

```console
curl -X GET "http://localhost:5000/urlinfo?query=http://royalmail-uk-deliveries.com%2Fbilling.php" -H "accept: application/json" -H "X-Api-Key: user-token-555"
```
The response payload is received with a 200 status code. The URL has been classified as **Ransomware**.
```shell
{
  "data": {
    "URL category": {
      "http://royalmail-uk-deliveries.com/billing.php": "Ransomware"
    }
  }, 
  "info": {
    "engine": {
      "version": "1.0"
    }, 
    "timestamp": "Sat, 20 Mar 2021 17:50:20 GMT"
  }, 
  "response_status": {
    "code": 200, 
    "message": "INFO: The request has succeeded."
  }
}
```
As a final example, we will lookup the following URL:
```console
curl -X GET "http://localhost:5000/urlinfo?query=www.o2billingfail.com/Login" -H "accept: application/json" -H "X-Api-Key: user-token-555"
```
The lookup categorizes this URL as Spyware, and a 200 status code is returned.
```shell
{
  "data": {
    "URL category": {
      "www.o2billingfail.com/Login": "Spyware"
    }
  }, 
  "info": {
    "engine": {
      "version": "1.0"
    }, 
    "timestamp": "Sat, 20 Mar 2021 17:57:54 GMT"
  }, 
  "response_status": {
    "code": 200, 
    "message": "INFO: The request has succeeded."
  }
} 
```
It is important to know that, in case the user does not provide an API authentication token, or if a wrong token is provided, following response will be send out with 401 Unauthorized status code.

```shell
{
  "data": "",
  "info": {
    "engine": {
      "version": "1.0"
    },
    "timestamp": "Sat, 20 Mar 2021 18:02:01 GMT"
  },
  "response_status": {
    "code": 401,
    "message": "ERROR: Unauthorized. The provided API token is not a valid registered token."
  }
}
```

## API Reference

The URL Lookup API service has a specification model defined based on Swagger, which is OpenAPI specification compliant.  

As per definition, the OpenAPI Specification (OAS) defines a standard, language-agnostic interface to RESTful APIs. An OpenAPI definition can then be used by documentation generation tools to display the API, code generation tools to generate servers and clients in various programming languages, testing tools, and many other use cases.

Once the service is deployed, navigate to http://<serverIP>:<serverPort>/apidocs to see and interact with the APIs and get familiar with the request and response models. This can also be used for visual testing and getting comfortable with using the APIs.

Once this specification page is visited, this is what is seen on the web browser page:

<img width="1672" alt="page1spec" src="https://user-images.githubusercontent.com/81005592/111889848-7f18be00-89a1-11eb-94ed-4e8fe25b7d8f.png">
<img width="1683" alt="page2spec" src="https://user-images.githubusercontent.com/81005592/111889850-82ac4500-89a1-11eb-9564-2a7ebb7b21f2.png">

Click on 'Try it out' and enter values in the query and X-Api-Key input sections, and click 'Execute'. The request and response content will be displayed as follows:

<img width="1669" alt="page3spec" src="https://user-images.githubusercontent.com/81005592/111889943-37defd00-89a2-11eb-926d-0cb4793e3b2d.png">
<img width="1671" alt="page4spec" src="https://user-images.githubusercontent.com/81005592/111889945-39a8c080-89a2-11eb-83d9-0fff12aef1d8.png">

## Troubleshooting Failures

All logging from the application code will be written to URL-api-engine.log in the same directory from where the service is being executed. Detailed logs regarding any failures and time of event, along with the call stack can be isolated in this log file.

Additional debuggging can be enabled by tuning the CLI flag on for enabling debug level logs. This is advised where a critical error needs to be isolated, where additional visibility into the functionality will be beneficial. 

To turn on debug level logs while deploying the application, pass the following flag as 1. By default, debug level logging is disabled. 

```shell
$ python3 URL-lookup-engine.py --debug 1 
```
Additionally, since this is a mission critical service as data path traffic will be waiting on the API service to function normally, any major errors should be flagged immediately and the administrator or on-call engineer notified. To enable this functionality, SMTP based email alert forwarding for major errors can be enabled as follows. By default, this feature stays turned off.

```shell
$ python3 URL-lookup-engine.py --email_alerts 1
```
A sample email notification will be as follows:
```shell
---------- MESSAGE FOLLOWS ----------
From: API-error-monitoring@URLService.com
To: engineer@company-name.com
Subject: ATTENTION : Critical Application Error - Action Needed!
Date: Sat, 20 Mar 2021 17:30:13 -0700
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable
MIME-Version: 1.0
X-Peer: 127.0.0.1

[2021-03-20 17:30:13,229] ERROR in URL-lookup-engine: Critical application error: Authentication service is not responding.
------------ END MESSAGE ------------
```


## Tests


## Contribute


## License
