from datetime import date

from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user

from utils.forms import AddPostForm, ContactForm, RegisterForm, CreatePostForm, LoginForm
from utils.utils import send_email, admin_only
from utils.models import BlogPost, User
from utils.db import db


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
Bootstrap5(app)
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


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
@admin_only
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
@admin_only
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
@admin_only
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You already signed up with that email, please log in.")
            return redirect(url_for('login'))
        pass_hash = generate_password_hash(form.password.data, salt_length=8)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=pass_hash
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if not user:
            flash("That email is invalid, please try again")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, form.password.data):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
