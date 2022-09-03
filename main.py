import os
from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, Register, Login, CommentForm
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("Blog_Secret_Key")
ckeditor = CKEditor(app)
gravatar = Gravatar(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLES
# class Users(UserMixin, db.Model):
#     __tablename__ = "Users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(250), nullable=False, unique=True)
#     password = db.Column(db.String(250), nullable=False)
#     name = db.Column(db.String(250), nullable=False)
#     posts = relationship("BlogPosts", back_populates="user")
#     comments = relationship("Comment", back_populates="user")
#
#
# class BlogPosts(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
#     user = relationship("Users", back_populates="posts")
#     user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
#     author = db.Column(db.String(250), nullable=False)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)
#     comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user = relationship("Users", back_populates="comments")
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    parent_post = relationship("BlogPosts", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    text = db.Column(db.Text, nullable=False)


db.create_all()


# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(user_id)


def admin_only(function):
    def is_admin():
        print(current_user.id)
        return function()
    return is_admin


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.id == 1:
                return f(*args, **kwargs)
        except:
            return "Unauthorized Access",403
    return decorated_function


## HOME PAGE/GET ALL POSTS
@app.route('/')
def get_all_posts():
    # posts = BlogPosts.query.all()
    posts = []
    return render_template("index.html", all_posts=posts)

# ## REGISTER TO THE BLOG
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = Register()
#     data = dict(request.form)
#     if request.method == "POST":
#         if form.validate_on_submit():
#             if Users.query.filter_by(email=data['email']).first() != None:
#                 flash("You've already signed up with this email. Login Instead")
#                 return redirect(url_for('login'))
#             pwd = generate_password_hash(data['password'])
#             user = Users(email=data['email'], password=pwd, name=data['name'])
#             db.session.add(user)
#             db.session.commit()
#             login_user(user)
#             # print(current_user.name)
#             return redirect(url_for('get_all_posts', logged_in=True))
#     return render_template("register.html", form=form)
#
#
# ## LOGIN
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = Login()
#     if request.method == "GET":
#         return render_template("login.html", form=form)
#     if request.method == "POST":
#         data = dict(request.form)
#         if form.validate_on_submit():
#             user = Users.query.filter_by(email=data['email']).first()
#             if user:
#                 if check_password_hash(user.password, data['password']):
#                     login_user(user)
#                     flash('Logged In Successfully!')
#                     return redirect(url_for('get_all_posts', logged_in=True))
#                 else:
#                     flash('Wrong Password for User')
#             else:
#                 flash('Wrong Email, Pls check again or Register Instead')
#         return render_template("login.html", form=form)
#
#
# ## LOGOUT
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('get_all_posts'))
#
#
# ## SHOW CERTAIN POST
# @app.route("/post/<int:post_id>", methods=['GET', 'POST'])
# def show_post(post_id):
#     requested_post = BlogPosts.query.get(post_id)
#     form = CommentForm()
#     comments = Comment.query.filter_by(post_id=requested_post.id).all()
#     if request.method == 'POST':
#         data = dict(request.form)
#         print(data)
#         if form.validate_on_submit:
#             if current_user.is_authenticated:
#                 print("Data is above")
#                 comment = Comment(user_id=current_user.id, post_id=requested_post.id, text=data['body'])
#                 db.session.add(comment)
#                 db.session.commit()
#             else:
#                 flash("Please Login to comment on the post")
#                 return redirect(url_for("login"))
#     return render_template("post.html", post=requested_post, form=form, comments=comments)
#
#
# ## NEW POST
# @app.route("/new-post", methods=['GET', 'POST'])
# def add_new_post():
#     form = CreatePostForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             new_post = BlogPosts(
#                 user_id = current_user.id,
#                 title=form.title.data,
#                 subtitle=form.subtitle.data,
#                 body=form.body.data,
#                 img_url=form.img_url.data,
#                 author=current_user,
#                 date=date.today().strftime("%B %d, %Y")
#             )
#             db.session.add(new_post)
#             db.session.commit()
#             return redirect(url_for("get_all_posts"))
#     return render_template("make-post.html", form=form)
#
#
# ## EDIT POST
# @app.route("/edit-post/<int:post_id>")
# @admin_only
# def edit_post(post_id):
#     post = BlogPosts.query.get(post_id)
#     edit_form = CreatePostForm(
#         title=post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=post.author,
#         body=post.body
#     )
#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.author = edit_form.author.data
#         post.body = edit_form.body.data
#         db.session.commit()
#         return redirect(url_for("show_post", post_id=post.id))
#
#     return render_template("make-post.html", form=edit_form)
#
#
# ## DELETE POST
# @app.route("/delete/<int:post_id>")
# @admin_only
# def delete_post(post_id):
#     post_to_delete = BlogPosts.query.get(post_id)
#     db.session.delete(post_to_delete)
#     db.session.commit()
#     return redirect(url_for('get_all_posts'))
#
#
# @app.route("/about")
# def about():
#     return render_template("about.html")
#
#
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
