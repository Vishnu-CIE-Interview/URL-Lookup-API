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


## How to use?


## Installation

The .env file contains the user configurable variables that the main API service will auto-configure for providing access to caching, database and email-alerting servers. 

Before deploying the server into production, change the following environmental variables listed in this file.

The initial values listed here are only placeholder entries.

The server key, credentials or IP addresses should NOT be exposed outside of the production server.

Contents of .env file that needs to be configured by the user:
```console
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

The following servers need to be set up before the main service can be initiated. 

### Memcached Server

The Memcached server should be accessible and routable to the network where the API production server is deployed. If the server chosen is a Debian/Ubuntu machine, the Memcached service can be installed on it using the command:

```console
$apt-get install memcached
```
Once installed, the caching end point can be initialized as follows by providing the port number. Once initialized, the caching layer will be connected to using the server’s IP and port address. This combination should be provided in the .env file as described earlier.

```console
$memcached -p 12345
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

## API Reference


## Tests


## Contribute


## License
