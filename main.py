from flask import Flask, render_template, request
from requests import get
from smtplib import SMTP
from email.message import EmailMessage


POSTS_API = "https://api.npoint.io/d567145ab9835ad1db9e"
response = get(POSTS_API).json()
MY_EMAIL = "Your email"
PASSWORD = "Your password"


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", posts=response)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:index>")
def view_post(index):
    for post in response:
        if post["id"] == index:
            return render_template("post.html", post=response[index - 1])


def send_email(name, email, phone, message):
    content = f"Name: {name}\n" \
              f"Email: {email}\n" \
              f"Phone: {phone}\n" \
              f"Message:{message}"
    msg = EmailMessage()
    msg["Subject"] = f"New message from {name}"
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL
    msg.set_content(content)
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.send_message(msg)


if __name__ == '__main__':
    app.run(debug=True)
