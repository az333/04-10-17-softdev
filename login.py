from flask import Flask, render_template, request

my_app = Flask(__name__)

username = "good"
password = "bad"
failure = ""

@my_app.route('/')
def root():
    return render_template('form.html')

@my_app.route('/submitted')
def submitted():
    if (request.args["name"] == username):
        if (request.args["pass"] == password):
            #success
            return render_template('success.html', name = request.args["name"])
        else:
            failure = "password"
    elif (request.args["pass"] == password):
        failure = "username"
    else:
        failure = "username and password"
    return render_template('fail.html', name = request.args["name"], fail = failure )

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
