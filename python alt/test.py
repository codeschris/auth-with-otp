from flask import Flask, render_template, request
import psycopg2
from psycopg2 import sql
import os
import string
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        otp = request.form.get('otp')

        if username is None or password is None:
            error = "Missing input. Input missing field(s)!"
        else:
            conn = psycopg2.connect(host='localhost',
                                    database='proj_db',
                                    user=os.environ['DB_USERNAME'],
                                    password=os.environ['DB_PASSWORD'])
            
            try:
                cursor = conn.cursor()
                query = sql.SQL("SELECT password FROM users WHERE name = %s")
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                if result is not None:
                    stored_password = result[0]

                    if password == stored_password or otp == password:
                        return render_template('landing.html')
                    else:
                        # generating lowercase and uppercase letters
                        bets_low = string.ascii_lowercase
                        bets_upper = string.ascii_uppercase
                        all_letters = bets_low + bets_upper  # joining lowercase and uppercase letters together
                        otp_code = ''.join(random.sample(all_letters, 5))  # randomizing letters and creating OTP code

                        error = 'OTP code is: {}'.format(otp_code)

                else:
                    error = "Invalid username or password."

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                error = "Database error: {}".format(str(e))
                
            finally:
                cursor.close()
                conn.close()

    return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)
