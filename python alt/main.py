from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import os
import bcrypt

app = Flask(__name__)
app.secret_key = b'schoolproject'

# Function to hash the password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect(url_for('landing'))
    
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
                cursor.execute(query, (username, ))
                user_data = cursor.fetchone()

                if user_data is not None:
                    stored_password = user_data[1]
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        session['username'] = user_data[0]
                        return redirect(url_for('landing'))
                else:
                    error = "Invalid username or password."

            except (psycopg2.Error, psycopg2.DatabaseError) as e:
                error = "Database error: {}".format(str(e))
                
            finally:
                cursor.close()
                conn.close()
        
    return render_template("index.html", error=error)

@app.route('/landing')
def landing():
    if 'username' in session:
        return render_template('landing.html', username=session['username'])
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
