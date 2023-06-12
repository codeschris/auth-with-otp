from flask import Flask, render_template, redirect, url_for, request
import string
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '':
            error = "Missing input. Input missing field(s)!"
        elif request.form['username'] != 'admin' or request.form['password'] != 'admin':
            #generating lowercase and uppercase letters
            bets_low = string.ascii_lowercase
            bets_upper = string.ascii_uppercase
            
            all = bets_low + bets_upper #joining lowercase and uppercase letters together

            list = random.sample(all, 5)    #randomizing letter and placing in a list
            result = ''.join(list)  #joining letters together to form a string

            error = 'OTP code is: {}'.format(result)    #passing OTP code incase of invalid details or forgotten password
        else:
            return redirect(url_for('index.html'))
        
    return render_template("index.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)