# Login Auth Site with OTP

- This is a project that contains a login auth page featuring non-functional OTP codes

## Python alt
The frontend has been created using basic form template from HTML and CSS (internal). No javascript has been using in the application.
The user keys in details contained in the database to grant them access to the landing page of the application. When the user enters the wrong details, they are provided with a (non-functional at the moment) one-time password so they can reset the password.

All passwords are stored within a Postgres Database and the backend operations are done with Flask. The OTP codes are generated randomly using a ramdomizer (created using the Python 'random' module) and the sample generated is displayed on the login page when the password and/or username are wrong.

### Dependencies
- flask
- random
- psycopg2
- string
- os
| Dependency  	| Function 	|
|---	|---	|
| flask  	|   	|
| random  	|   	|
| psycopg2  	|   	|
| os  	|   	|
| string  	|   	|
_will update this soon..._
