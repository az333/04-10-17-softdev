from flask import Flask, render_template, request, session, redirect, url_for
import os, csv

my_app = Flask(__name__)

my_app.secret_key = os.urandom(32)

username = ""
password = ""
failure = ""
success = ""
logindict = {};

@my_app.route('/', methods=['GET', 'POST'])
def root():
    global failure, success, username, password
    if (session.get(username) == password):
        return render_template('welcome.html', name = username)
    elif (failure != ""):
        failtemp = failure
        failure = ""
        return render_template('login.html', fail = failtemp)
    elif (success != ""):
        suctemp = success
        success = ""
        return render_template('login.html', success = suctemp)
    else:
        return render_template('login.html')

@my_app.route('/submitted', methods=['GET','POST'])
def submitted():
    global failure, username, password
    failure = "Your login was not succesful. You entered the incorrect "
    user = request.form["name"]
    passy= request.form["pass"]
    if (user in logindict):
        if (request.form["pass"] == logindict[user]):
            #success
            failure = ""
            session[user] = passy
            username = user
            password = passy
            return redirect("/")
            #return render_template('welcome.html', name = request.form["name"])
        else:
            #wrong password
            failure += "password."
    else:
        #wrong username AND password
        failure += "username."
    return redirect('/')

@my_app.route('/registration', methods=['GET','POST'])
def register():
    return render_template("register.html")

@my_app.route('/submitregister', methods= ['GET', 'POST'])
def submitregister():
    global success
    if (request.form["newpass"] != request.form["repeatpass"]):
        return render_template("register.html", repeatfail = "Your passwords do not match. Please try again.")
    else:
        logindict[request.form["newuser"]] = request.form["newpass"]
        success = "You have successfully registered your account! You may log in now."
        return redirect("/")

@my_app.route('/loggedout', methods=['GET','POST'])
def logout():
    if (session.get(username)==password):
        session.pop(username)
    return redirect("/")

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
