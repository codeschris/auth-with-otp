# Login Auth Site with OTP
- This is a project that contains a login auth page featuring non-functional OTP codes

# Requirements
- Python v3.11
- PostgresQL

# Alternatives: 
1. Python
2. PHP

## 1. Python Alternative
The frontend has been created using basic form template from HTML and CSS (internal). No javascript has been using in the application.
The user keys in details contained in the database to grant them access to the landing page of the application. When the user enters the wrong details, they are provided with a (non-functional at the moment) one-time password so they can reset the password.

All passwords are stored within a Postgres Database and the backend operations are done with Flask. The OTP codes are generated randomly using a ramdomizer (created using the Python 'random' module) and the sample generated is displayed on the login page when the password and/or username are wrong.

| Dependency used | Function                                                       |
| ---------- | -------------------------------------------------------------- |
| flask      | Handling property access and backend operations                |
| psycopg2   | Connecting and accessing Postgres database                     |
| string     | Acquiring ASCII alphabets in lowercase and uppercase           |
| random     | Generating a random sample of alphabets from list of alphabets |
| os         | Accessing critical information from system user variables      |

### To do:
- [x] Add OTP feature to application
- [x] Connecting database to application
- [ ] Hashing passwords

_The application/webpage was created for operations and testing within localhost so it is free to fork/clone this repository and modify. Thank you!_

## 2. PHP alternative

_Will update this soon..._
