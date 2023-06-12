from flask import Flask, render_template, redirect, url_for, request
import psycopg2
from psycopg2 import sql
import os
import string
import random

#connect to the database using sqlalchemy
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username is None or password is None:
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
                    return redirect(url_for('index'))
                else:
                    #generating lowercase and uppercase letters
                    bets_low = string.ascii_lowercase
                    bets_upper = string.ascii_uppercase
            
                    all = bets_low + bets_upper #joining lowercase and uppercase letters together

                    list = random.sample(all, 5)    #randomizing letter and placing in a list
                    result = ''.join(list)  #joining letters together to form a string

                    error = 'OTP code is: {}'.format(result)    #passing OTP code incase of invalid details or forgotten password

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                error = "Database error: {}".format(str(e))
            finally:
                cursor.close()
                conn.close()

    return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)