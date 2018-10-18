from flask import Flask,render_template,session,request,url_for,redirect,flash
import os, sqlite3, csv
app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = "./Big_Daddy.db"
db = sqlite3.connect(DATABASE)
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS logins (username TEXT, password TEXT)")
#checks the credentials against the hard coded user
#def check_credentials(username,password):
 #   return username == user1 and password == pass1

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

@app.route('/login')
def log():
    return render_template("login.html")

@app.route("/auth",methods=["POST"])
def authenticate():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logins(username TEXT, password TEXT)")
    c.execute("INSERT INTO logins VALUES(\"asd\",\"asd\")")
    c.execute("INSERT INTO logins VALUES(\"val\",\"val\")")
    c.execute("SELECT * FROM logins")
    usrs = c.fetchone()

    while usrs != None:
        print(usrs[0] + "," + usrs[1])
        if usrs[0] == request.form.get('username') and usrs[1] == request.form.get('password'):
            db.commit()
            db.close()
            return redirect(url_for('log'))
        else:
            usrs = c.fetchone()
    print("Nothing")
    db.commit()
    db.close()
    return redirect(url_for('home'))

@app.route("/home")
def blogHome():
    return render_template("base.html", title = "SUCCESS", content = "YAT", footer = "YAT")












if __name__ == "__main__":
    app.debug = True
    app.run()
