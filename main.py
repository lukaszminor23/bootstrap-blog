from datetime import date

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

from utils.forms import ContactForm, AddPostForm
from utils.email import send_email
from utils.post_model import BlogPost
from utils.db import db


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
Bootstrap5(app)
ckeditor = CKEditor(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    with app.app_context():
        all_posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", posts=all_posts)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(
            form.name.data,
            form.email.data,
            form.phone.data,
            form.message.data
        )
        return render_template("contact.html", msg_sent=True, form=form)
    return render_template("contact.html", msg_sent=False, form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:post_id>")
def view_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


@app.route("/make-post", methods=['GET', 'POST'])
def make_post():
    form = AddPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('make-post.html', form=form)


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    form = AddPostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('make-post.html', form=form, is_edit=True)


@app.route("/delete-post/<int:post_id>")
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
