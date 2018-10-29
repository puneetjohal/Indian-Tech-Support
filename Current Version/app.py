from flask import Flask,render_template,session,request,url_for,redirect,flash
import os, sqlite3, csv, time
from random import choice
app = Flask(__name__)
app.secret_key = os.urandom(32)

DATABASE = "./Big_Daddy.db"

@app.route('/')
def home():
    if 'user' in session: #sessioning
        return redirect(url_for('blogHome')) #if there is somebody logged in, then redirect them to hte home page
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    featured = []
    try:
        c.execute("SELECT * FROM blogs")
        featured = c.fetchall()
        if len(featured) > 0:
            featured = choice(featured) #if blogs exist, then choose a blog to be the "featured blog"
    except Exception as e:
        print("table doesn't exist")
        featured = "" # but if there aren't any blogs, then it returns an empty string
    return render_template("LandingTemplate.html",
                            Title = "Humblr",
                            heading = "Welcome to Humblr",
                            desc = "Get Humbled",
                            randPost = featured)

@app.route("/logout")
def logout():
    #removes the user from the session
    session.pop('user')
    #redirects to the home page after logging user out
    return redirect(url_for('home'))

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
            #request.cookies[request.form.get('username')]
            #request.cookies[request.form.get('password')]
            session['user'] = item[0]
            return redirect(url_for('blogHome'))
    print("Nothing")
    db.close()
    flash("Unknown username or password! Please try again") #usr and pass combo not in table
    return redirect(url_for('log'))

@app.route("/home")
def blogHome():
    #substitute until we get blog homepage working
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS blogs(users TEXT, content TEXT, time_of_blog TEXT, tags TEXT)")
    #c.execute("INSERT INTO blogs VALUES(\"username\",\"asdasdasdasd\")")
    c.execute("SELECT * FROM blogs WHERE users = {}".format('''"''' + session.get('user') + '''"''')) #since session.get('user') doesn't include the quotes, we put the quotes around it
    user_blogs = c.fetchall()
    ordered_blogs = []
    for i in range(len(user_blogs) - 1, -1, -1):
        ordered_blogs.append(user_blogs[i]) #adds blog in order
    user_blogs = ordered_blogs
    db.commit()
    db.close()
    return render_template("blog_home.html", title = session.get('user'), content = user_blogs, user = session.get('user'))

@app.route('/make-blog')
def new_blog_page():
    return render_template("new-blog.html")

@app.route('/blog-create')
def create_blog():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    usr = session.get('user')
    tags = request.args.get('tags')
    content = request.args.get('content')
    blogTime = time.asctime(time.localtime()) #to print the time
    tags = usr + "," + tags
    print(content)
    c.execute("INSERT INTO blogs VALUES(\"{}\",\"{}\", \"{}\",\"{}\")".format(usr, content, blogTime, tags)) #adds features to database
    db.commit()
    db.close()
    flash("Congratulations, you have made a new blog!\n")
    return redirect(url_for('blogHome'))

@app.route('/search')
def search():
    if 'user' not in session: #if not logged in
        return redirect(url_for('home'))
    db =sqlite3.connect(DATABASE)
    c = db.cursor()
    search_content = request.args.get('search')
    tags = search_content.split(",")
    c.execute("CREATE TABLE IF NOT EXISTS blogs(users TEXT, content TEXT, time_of_blog TEXT, tags TEXT)") #incase the table doesn't exist, make one
    c.execute("SELECT * FROM blogs")
    all_tags = c.fetchall()
    correct_tags = []
    for blog in all_tags:
        for tag in tags:
            if tag in blog[3]:
                correct_tags.append(blog)
    print(correct_tags)
    if len(correct_tags) < 0:
        flash("Internal Sever Error")
    if len(correct_tags) == 0:
        flash("No posts found :(") #if there aren't any tags
    return render_template('blog_home.html', content = correct_tags, user = session.get('user'))

@app.route('/edit')
def update():
    if 'user' not in session: #if not logged in
        return redirect(url_for('home'))
    #print(request.args.get('content'))
    content = request.args.get('content')
    OGtime = request.args.get('time')
    #print(OGtime)
    return render_template('edit_blog.html', content = content, post = OGtime)

@app.route('/edit-auth')
def edit():
    if 'user' not in session: #if not logged in
        return redirect(url_for('home'))
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    content = request.args.get('content')
    searched_for_time = request.args.get('time')
    #print(request.args.get('content'))
    #print(searched_for_time)
    c.execute("SELECT * FROM blogs WHERE time_of_blog=\"{}\"".format(searched_for_time)) #searching for the time of blog
    #test = c.fetchall()
    #print("this is the whole thing\n")
    #print(test)
    #print(time.asctime(time.localtime()))
    c.execute("UPDATE blogs SET content =\"{}\", time_of_blog =\"{}\" WHERE time_of_blog=\"{}\"".format(content, time.asctime(time.localtime()), searched_for_time)) #updates content and time
    #print(searched_for_time)
    db.commit()
    db.close()
    flash("Everything's looking good! Blog has been updated!") #once editing is  completed
    return redirect(url_for('blogHome'))





if __name__ == "__main__":
    app.debug = True
    app.run()
