# Login Auth Site with OTP

- This is a project that contains a login auth page featuring non-functional OTP codes

## Requirements

- Python v3.10 onwards
- PostgresQL

## Description

The frontend has been created using basic form template from HTML and CSS (internal). No javascript has been using in the application.
The user keys in details contained in the database to grant them access to the landing page of the application. When the user enters the wrong details, they are provided with a one-time password they can use as a log-in alternative for the forgotten/wrong password.

All passwords are stored within a Postgres Database and the backend operations are done with Flask. The OTP codes are generated randomly using a randomizer (created using the Python 'random' module) and the sample generated is displayed on the login page when the password and/or username are wrong.

| Dependency used | Function                                                       |
| ---------- | -------------------------------------------------------------- |
| flask      | Handling property access and backend operations                |
| psycopg2   | Connecting and accessing Postgres database                     |
| string     | Acquiring ASCII alphabets in lowercase and uppercase           |
| random     | Generating a random sample of alphabets from list of alphabets |
| os         | Accessing critical information from system user variables      |

### Important note

Remember to set user variables in the terminal for ease of identification of variables declared during execution:

```shell
export DB_NAME = 'database_name'
export DB_PASSWORD = 'password'
export DB_USERNAME = 'database_username'
```

### Checklist

- [x] Add OTP feature to application
- [x] Enable OTP functionality
- [x] Connecting database to application
- [x] Hashing passwords
