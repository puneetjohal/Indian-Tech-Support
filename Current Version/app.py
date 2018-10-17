from flask import Flask,render_template,session,request,url_for,redirect,flash
import os
app = Flask(__name__)
app.secret_key = os.urandom(32)

#hardcoded user
user1 = "tester"
pass1 = "test"

#checks the credentials against the hard coded user
def check_credentials(username,password):
    return username == user1 and password == pass1

@app.route('/')
def home():
    return render_template("LandingTemplate.html",
                            Title = "Humblr",
                            heading = "Welcome to Humblr",
                            desc = "Get Humbled")
@app.route("/logout")
def logout():
    #removes the user from the session
    session.pop("user")
    #redirects to the home page after logging user out
    return redirect(url_for('home'))

@app.route("/auth",methods=["POST"])
def authenticate():
    error = ""
    username = request.form['username']
    password = request.form['password']
    #if the credentials match, add the user to session
    if check_credentials(username,password):
        session["user"] = username
    #checks for bad username
    else:
        error = "Unknown user, please try again"
        #flashes error
        flash(error)
    #redirects to home
    return redirect(url_for('home'))
@app.route("/home")
def blogHome():













if __name__ == "__main__":
    app.debug = True
    app.run()
