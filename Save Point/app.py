from flask import Flask, request, flash, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("LandingTemplate.html",
                            Title = "Humblr",
                            heading = "Welcome to Humblr",
                            desc = "Get Humbled")















if __name__ == "__main__":
    app.debug = True
    app.run()
