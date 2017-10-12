from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, csv

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

failure = ""
success = ""
logindict = {}

with open('data/logins.csv', mode='r') as infile:
    reader = csv.reader(infile)
    logindict = {rows[0]:rows[1] for rows in reader}


@my_app.route('/', methods=['GET', 'POST'])
def root():
    global failure, success
    if ('user' in session):
        return render_template('welcome.html', name = session['user'])
    elif (failure != ""):
        failtemp = failure
        failure = ""
        flash(failtemp)
        return render_template('login.html')
    elif (success != ""):
        suctemp = success
        success = ""
        flash(suctemp)
        return render_template('login.html')
    else:
        return render_template('login.html')

@my_app.route('/submitted', methods=['GET','POST'])
def submitted():
    global failure
    failure = "Your login was not succesful. You entered the incorrect "
    user = request.form["name"]
    passwrd= request.form["pass"]
    if (user in logindict):
        if (passwrd == logindict[user]):
            #success
            failure = ""
            session['user'] = user
        else:
            #wrong password
            failure += "password."
    else:
        #wrong username\
        failure += "username."
    return redirect(url_for('root'))

@my_app.route('/registration', methods=['GET','POST'])
def register():
    return render_template("register.html")

@my_app.route('/submitregister', methods= ['GET', 'POST'])
def submitregister():
    global success
    username = request.form["newuser"]
    passwrd = request.form["newpass"]
    if (passwrd != request.form["repeatpass"]):
        return render_template("register.html", registerfail = "Your passwords do not match. Please try again.")
    else:
        if  (username not in logindict):
            logindict[username] = passwrd
            with open('data/logins.csv','a') as f:
                w = csv.writer(f)
                w.writerow([username,passwrd])
                f.close()
                success = "You have successfully registered your account! You may log in now."
                return redirect(url_for("root"))
        else:
            flash("An account with that username already exists. Please try again.")
            return render_template("register.html")


@my_app.route('/loggedout', methods=['GET','POST'])
def logout():
    if ('user' in session):
        session.pop('user')
    return redirect(url_for("root"))

@my_app.route('/delete', methods=['GET', 'POST'])
def delete():
    username = session['user']
    logindict.pop(username)
    
    return


if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
