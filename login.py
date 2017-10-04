from flask import Flask, render_template, request, session
import os

my_app = Flask(__name__)

my_app.secret_key = os.urandom(32)

username = "john"
password = "doe"

@my_app.route('/', methods=['GET', 'POST'])
def root():
    if (session.get(username) == password):
        return render_template('welcome.html', name = username)
    else:
     return render_template('login.html')

@my_app.route('/submitted', methods=['GET','POST'])
def submitted():
    failure = "Your login was not succesful. You entered the incorrect "
    if (request.form["name"] == username):
        if (request.form["pass"] == password):
            #success
            session["john"] = "doe"
            return render_template('welcome.html', name = request.form["name"])
        else:
            #wrong password
            failure += "password"
    elif (request.form["pass"] == password):
        #wrong username
        failure += "username"
    else:
        #wrong username AND password
        failure += "username and password"
    return render_template("login.html", fail = failure)

@my_app.route('/loggedout', methods=['GET','POST'])
def logout():
    session.pop("john")
    return render_template("login.html")

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
