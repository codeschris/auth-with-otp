import random
from flask import Flask, render_template, request
import psycopg2
from psycopg2 import sql
import os
import string

app = Flask(__name__)

def generate_random_otp():
    bets_low = string.ascii_lowercase
    bets_upper = string.ascii_uppercase
    all_letters = bets_low + bets_upper
    otp_code = ''.join(random.sample(all_letters, 5))
    return otp_code

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    otp_generated = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '':
            error = "Missing input. Input missing field(s)!"
        else:
            conn = psycopg2.connect(host='localhost',
                            database='proj_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
            
            try:
                cursor = conn.cursor()
                query = sql.SQL("SELECT password, otp_code FROM users WHERE name = %s")
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                if result:
                    stored_password, otp_code = result

                    if password == stored_password:
                        return render_template('landing.html')
                    elif password == otp_code:
                        return render_template('landing.html', login_method='OTP')
                    else:
                        code = generate_random_otp()
                        error = "Invalid password or OTP. OTP code is {}".format(code)
                        update_query = sql.SQL("UPDATE users SET otp_code = %s WHERE name = %s")
                        cursor.execute(update_query, (code, username))
                        conn.commit()
                else:
                    error = "User not found."

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                error = "Database error: {}".format(str(e))
                
            finally:
                cursor.close()
                conn.close()
    
    return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)
