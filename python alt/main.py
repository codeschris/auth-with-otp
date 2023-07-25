from flask import Flask, render_template, request
import psycopg2
from psycopg2 import sql
import os
import string
import random
import bcrypt

app = Flask(__name__)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def update_passwords():
    conn = psycopg2.connect(host='localhost',
                            database = 'proj_db',
                            user = os.environ['DB_USERNAME'],
                            password = os.environ['DB_PASSWORD'])
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name, password FROM users")
        rows = cursor.fetchall()

        for row in rows:
            username, plain_password = row
            hashed_password = hash_password(plain_password)
            cursor.execute("UPDATE users SET password = %s WHERE name = %s", (hashed_password, username))
            conn.commit()
    except (psycopg2.Error, psycopg2.DatabaseError) as e:
        print("Database error: {}".format(str(e)))

    finally:
        cursor.close()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':
            error = "Missing input. Input missing field(s)!"
        else:
            conn = psycopg2.connect(host='localhost',
                            database='proj_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
            
            try:
                cursor = conn.cursor()
                query = sql.SQL("SELECT COUNT(*) FROM users WHERE name = %s AND password = %s")
                cursor.execute(query, (username, password))
                result = cursor.fetchone()[0]

                if result == 1:
                    return render_template('landing.html')
                else:
                    #generating lowercase and uppercase letters
                    bets_low = string.ascii_lowercase
                    bets_upper = string.ascii_uppercase
                    all = bets_low + bets_upper #joining lowercase and uppercase letters together
                    list = random.sample(all, 5)    #randomizing letter and placing in a list
                    res = ''.join(list)  #joining letters together to form a string

                    #passing OTP code incase of invalid details or forgotten password
                    error = 'OTP code is: {}'.format(res)

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                error = "Database error: {}".format(str(e))
                
            finally:
                cursor.close()
                conn.close()
        
    return render_template("index.html", error=error)

if __name__ == '__main__':
    update_passwords()
    app.run(debug=True)