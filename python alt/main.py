from flask import Flask, render_template, request
import psycopg2
import os
import string
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

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
                query = "SELECT name, password FROM users WHERE name = %s"
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()

                if user_data is not None:
                    stored_password = user_data[1]
                    if check_password_hash(stored_password, password):
                        return render_template('landing.html')
                    else:
                        # Generating lowercase and uppercase letters
                        bets_low = string.ascii_lowercase
                        bets_upper = string.ascii_uppercase
                        all_chars = bets_low + bets_upper
                        random_chars = random.sample(all_chars, 5)
                        otp_code = ''.join(random_chars)
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
