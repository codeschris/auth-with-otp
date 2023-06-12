from flask import Flask, render_template, redirect, url_for, request
import psycopg2
import os
import string
import random

#connect to the database using sqlalchemy

def get_db_conn():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '':
            error = "Missing input. Input missing field(s)!"
        elif request.form['username'] != 'admin' or request.form['password'] != 'admin':    #change arguments for user and pass
            #generating lowercase and uppercase letters
            bets_low = string.ascii_lowercase
            bets_upper = string.ascii_uppercase
            
            all = bets_low + bets_upper #joining lowercase and uppercase letters together

            list = random.sample(all, 5)    #randomizing letter and placing in a list
            result = ''.join(list)  #joining letters together to form a string

            error = 'OTP code is: {}'.format(result)    #passing OTP code incase of invalid details or forgotten password
        else:
            return redirect(url_for('index'))
        
    return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)