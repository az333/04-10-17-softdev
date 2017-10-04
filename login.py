from flask import Flask, render_template, request

my_app = Flask(__name__)

username = "john"
password = "doe"
failure = ""

@my_app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('form.html')

@my_app.route('/submitted', methods=['GET','POST'])
def submitted():
    if (request.form["name"] == username):
        if (request.form["pass"] == password):
            #success
            return render_template('success.html', name = request.form["name"])
        else:
            failure = "password"
    elif (request.form["pass"] == password):
        failure = "username"
    else:
        failure = "username and password"
    return render_template('fail.html', name = request.form["name"], fail = failure )

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
