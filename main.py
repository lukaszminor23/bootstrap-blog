import datetime
from datetime import date

from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from modules.forms import AddPostForm, ContactForm, RegisterForm, LoginForm, CommentForm
from modules.utils import send_email, admin_only
from modules.models import BlogPost, User, Comment
from config import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


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


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def view_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                text=form.comment.data,
                author=current_user,
                post=requested_post,
                time=datetime.datetime.now()
            )
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash("You must be logged in to post comments. Please log in.")
            return redirect(url_for('login'))
    return render_template("post.html", post=requested_post, form=form)


@app.route("/make-post", methods=['GET', 'POST'])
@admin_only
def make_post():
    form = AddPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            author=current_user,
            body=form.body.data,
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
        img_url=post.img_url,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('make-post.html', form=form, is_edit=True)


@app.route("/delete-post/<int:post_id>")
@admin_only
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)
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





if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
