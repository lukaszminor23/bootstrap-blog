from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class AddPostForm(FlaskForm):
    title = StringField("Blog post title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your name", validators=[DataRequired()])
    img_url = StringField("Blog image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog content", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ContactForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    email = StringField("Your email", validators=[DataRequired(), Email()])
    phone = StringField("Your phone number", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send message")
