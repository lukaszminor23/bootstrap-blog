from flask import Flask, render_template
from requests import get


POSTS_API = "https://api.npoint.io/d567145ab9835ad1db9e"
response = get(POSTS_API).json()


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", posts=response)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
