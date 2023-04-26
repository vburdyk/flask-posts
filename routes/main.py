from app import app, db, manager
from flask import render_template, request, redirect, flash, url_for
from models import User, Post
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def hello_world():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")


@app.route("/save-user", methods=["POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if not (email or password or first_name or last_name):
            flash("Please fill all fields")

        pass_hash = generate_password_hash(password)
        new_user = User(email=email,
                        password=pass_hash,
                        first_name=first_name,
                        last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('hello_world'))


@app.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")


@app.route("/authorize", methods=["POST"])
def authorize():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                next_page = request.args.get('next')

                return redirect(next_page or url_for('hello_world'))
            else:
                flash("Password or email is not correct")
                return redirect(url_for('sign_in'))
        else:
            flash("Need email and password")
            return redirect(url_for('sign_in'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('sign_in') + '?next=' + request.url)
    return response


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("hello_world"))


@app.route("/upload")
@login_required
def upload():
    return render_template("upload-post.html")


@app.route("/upload-submit", methods=['POST'])
@login_required
def upload_submit():
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('body')
        author = current_user.get_id()
        new_post = Post(title=title,
                        body=body,
                        author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('hello_world'))


@app.route("/delete-post/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.get_id() == str(post.author):
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('hello_world'))
    return redirect(url_for('hello_world'))


@app.route("/edit-post", methods=["GET"])
@login_required
def edit_post():
    post_id = request.args.get('post')
    post = Post.query.get(post_id)
    if current_user.get_id() == str(post.author):
        return render_template('edit-post.html', post=post)
    else:
        return redirect(url_for('hello_world'))


@app.route("/edit-post-apply", methods=["POST"])
@login_required
def edit_post_apply():
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        body = request.form.get('body')
        title = request.form.get('title')
        post = Post.query.get(post_id)
        if current_user.get_id() == str(post.author):
            post.body = body
            post.title = title
            db.session.commit()
            return redirect(url_for('hello_world'))
        else:
            return redirect(url_for('hello_world'))
