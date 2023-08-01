import random
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql
import os
import string
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

#One time password generator
def generate_random_otp():
    bets_low = string.ascii_lowercase
    bets_upper = string.ascii_uppercase
    all_letters = bets_low + bets_upper
    otp_code = ''.join(random.sample(all_letters, 5))
    return otp_code

#hashing function
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, password)

#redirection route
@app.route('/index.html')
def redirection():
    return redirect(url_for('index'))

#main route
@app.route('/login', methods=['GET', 'POST'])
def index():
    error = None

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

                    if verify_password(password, stored_password.encode('utf-8')):
                        return render_template('landing.html')
                    elif password == otp_code:
                        return render_template('landing.html')
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':
            error = "Missing details. Input missing field(s)"
        else:
            conn = psycopg2.connect(host = 'localhost',
                                    database = 'proj_db',
                                    user = os.environ['DB_USERNAME'],
                                    password=os.environ['DB_PASSWORD'])
            try:
                cursor = conn.cursor()
                query = sql.SQL('SELECT COUNT(*) FROM users WHERE name = %s')
                cursor.execute(query, (username,))
                count = cursor.fetchone()[0]

                if count > 0:
                    error = "Username already exists. Choose a different username."
                else:
                    hashed_password = hash_password(password)
                    insert_query = sql.SQL("INSERT INTO users (name, password) VALUES (%s, %s)")
                    cursor.execute(insert_query, (username, hashed_password))
                    conn.commit()
                    return render_template('index.html', message="Registration Successful")
                
            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                error = "Database error: {}".format(str(e))
            
            finally:
                cursor.close()
                conn.close()
    
    return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
