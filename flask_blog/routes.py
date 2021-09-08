from flask_blog.models import User,Post
from flask import render_template,url_for,flash,redirect,request,abort
from flask_blog.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostFrom
from flask_blog import app,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image


@app.route('/')
@app.route('/home')
def home():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About Page')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,mobile=form.mobile.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! Now you are able to login','success')
        # flash(f'Account Created for {form.mobile.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful please check you email id or password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    f_name,f_ext=os.path.splitext(form_picture.filename)
    picture_name=random_hex + f_ext
    picture_path=os.path.join(app.root_path,'static/profile',picture_name)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.mobile=form.mobile.data
        db.session.commit()
        flash('Your Account has been updated','success')
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile
    image_file=url_for('static',filename='profile/' + current_user.image_file )
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=PostFrom()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',form=form, legeng='Create Post')

@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form=PostFrom()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your messsage has been updated !','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html', title='Update Post', form=form, legeng='Update Post')

@app.route("/post/<int:post_id>/delete",methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post deleted sucessfully','info')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_post(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template('user_posts.html',posts=posts,user=user)