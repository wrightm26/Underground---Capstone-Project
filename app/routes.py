
import os
from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import SignUpForm, LoginForm, AddArtForm, UploadForm
from werkzeug.utils import secure_filename
from app.models import User, Art
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    files = os.listdir(f"{app.config['UPLOAD_PATH']}")
    arts = Art.query.all()
    return render_template('index.html', files=files, arts=arts)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray our form was validated!!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)

        check_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalars().all()
        if check_user:

            flash("A user with that username and/or email already exists", "warning")
            return redirect(url_for('signup'))

        new_user = User(first_name=first_name, last_name=last_name, address=address, city=city, state=state, zipcode=zipcode, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :')
        username = form.username.data
        password = form.password.data
        print(username,password)
        user= User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'You have succesfully logged in as {username}!', "success")
            return redirect(url_for('index'))
        else:
            flash(f'Invalid username or password', "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/profile/<username>')
def profile(username):
    profile = User.query.filter_by(username=username).first()
    text_to_copy = 'http://127.0.0.1:5000/profile/{profile.username}'
    if profile is None:
        return redirect(url_for('signup'))
    else:
        arts = Art.query.all()
        return render_template('profile.html', username=username, arts=arts, profile=profile)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))

@app.route('/upload/<artwork_id>', methods=["GET", "POST"])
@login_required
def upload_file(artwork_id):
    form = UploadForm()
    if form.validate_on_submit():
        uploaded_file = request.files['image']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            art = Art.query.get(artwork_id)
            art.image = filename
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)



@app.route('/addart', methods=['GET','POST'])
@login_required
def addart():
    form  = AddArtForm()
    if form.validate_on_submit():
        title = form.title.data
        width = form.width.data
        height = form.height.data
        description = form.description.data
        price = form.price.data

        new_art = Art(title=title, width=width, height=height, description=description, price=price, user_id=current_user.id)
        print("New artwork added")

        flash(f"{new_art.title} has been created!", "success")

        return redirect(url_for('upload_file', artwork_id=new_art.art_id))
    return render_template('addart.html', form=form)

@app.route('/delete/<art_id>')
@login_required
def delete_art(art_id):
    art_to_delete = Art.query.get_or_404(art_id)
    if art_to_delete.user_id != current_user.id:
        print("You do not have permission to delete this post")
        flash("You do not have permission to delete this post", "danger")

        return redirect(url_for('index'))

    db.session.delete(art_to_delete)
    db.session.commit()
    flash(f"{art_to_delete.title} has been deleted", "info")
    print("You have been deleted")
    return redirect(url_for('index'))

@app.route('/edit/<art_id>', methods=["GET", "POST"])
@login_required
def edit_art(art_id):
    form = AddArtForm()
    art_to_edit = Art.query.get_or_404(art_id)
    if art_to_edit.user_id != current_user.id:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))

    if form.validate_on_submit():
        art_to_edit.title = form.title.data
        art_to_edit.width = form.width.data
        art_to_edit.height = form.height.data
        art_to_edit.description = form.description.data
        art_to_edit.price = form.price.data

        db.session.commit()
        flash(f"{art_to_edit.title} has been edited!", "success")
        return redirect(url_for('upload'))

    form.title.data = art_to_edit.title
    form.width.data = art_to_edit.width
    form.height.data = art_to_edit.height
    form.description = art_to_edit.description.data
    form.price.data = art_to_edit.price.data

    return render_template('edit.html', form=form, art=art_to_edit)
