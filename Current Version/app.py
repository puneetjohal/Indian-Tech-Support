from flask import Flask,render_template,session,request,url_for,redirect,flash
import os, sqlite3, csv
app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = "./Big_Daddy.db"

@app.route('/')
def home():
    if 'user' in session: #sessioning
        return redirect(url_for('blogHome'))
    return render_template("LandingTemplate.html",
                            Title = "Humblr",
                            heading = "Welcome to Humblr",
                            desc = "Get Humbled")
@app.route("/logout")
def logout():
    #removes the user from the session
    session.pop("user")
    #redirects to the home page after logging user out
    return redirect(url_for('/'))

@app.route('/login')
def log():
    return render_template("login.html")

@app.route('/register') #registry, displayed page still WIP
def register():
    return render_template("registerPage.html")

@app.route('/register-auth', methods=["POST"])
def regis_auth(): #check if registration is correctly done
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logins(username TEXT, password TEXT)") #if this our first member, welcome!
    c.execute("SELECT * FROM logins")
    people = c.fetchall()
    #shorthanding
    usr = request.form.get('username')
    paswrd = request.form.get('password')
    confirm = request.form.get('confirm')
    for item in people: #item is a tuple, can be indexed
        if item[0] == None or item[1] == None: #empty form submitted
            flash("Please enter a username/password")
            return redirect(url_for('register'))
        if item[0] == usr: #username is already in table, not unique
            flash("Username taken! Try a different one")
            return redirect(url_for('register'))
        if paswrd != confirm: #password doesn't match the confirmation
            flash("Passwords do not match! Please try again")
            return redirect(url_for('register'))
    c.execute("INSERT INTO logins VALUES(\"{}\",\"{}\")".format(usr, paswrd)) #everything is a okie
    flash("Congratulations on getting a Humblr account! Now, let's be Humbled together")
    db.commit()
    db.close()
    return redirect(url_for('log')) #go back to login page

@app.route("/auth",methods=["POST"])
def authenticate():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logins(username TEXT, password TEXT)") #make sure next line doesn't cause crash
    c.execute("SELECT * FROM logins")
    usrs = c.fetchall() #logins now is check iteratively by FOR instead of WHILE
    for item in usrs:
        if request.form.get('username') == item[0] and request.form.get('password') == item[1]:
            request.cookies[request.form.get('username')]
            request.cookies[request.form.get('password')]
            session['user'] = item[0]
            return redirect(url_for('blogHome'))
    print("Nothing")
    db.close()
    flash("Unknown username or password! Please try again") #usr and pass combo not in table
    return redirect(url_for('log'))

@app.route("/home")
def blogHome():
    #substitute until we get blog homepage working
    #db = sqlite3.connect()
    #c = db.cursor()
    #c.execute("CREATE TABLE IF NOT EXISTS blogs(users TEXT, content TEXT)")
    #c.execute("SELECT * FROM blogs WHERE users = {}".format())
    #user_blogs = c.fetchall()

    return render_template("blog_home.html", title =request.cookies.get('username'), content = "YAT", footer = "YAT")












if __name__ == "__main__":
    app.debug = True
    app.run()
