from flask import Flask, render_template, request, session
import os

my_app = Flask(__name__)

my_app.secret_key = os.urandom(32)

username = "john"
password = "doe"
failure = ""


@my_app.route('/', methods=['GET', 'POST'])
def root():
    if (session.get("john") == "doe"):
        return render_template('welcome.html')
    else:
     return render_template('login.html')

@my_app.route('/submitted', methods=['GET','POST'])
def submitted():
    if (request.form["name"] == username):
        if (request.form["pass"] == password):
            #success
            session["john"] = "doe"
            return render_template('success.html', name = request.form["name"])
        else:
            #wrong password
            failure = "password"
    elif (request.form["pass"] == password):
        #wrong username
        failure = "username"
    else:
        #wrong username AND password
        failure = "username and password"
    return render_template('fail.html', name = request.form["name"], fail = failure )

@my_app.route('/loggedout', methods=['GET','POST'])
def logout():
    session.pop("john")
    return render_template("login.html")

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
