
import os
from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import SignUpForm, LoginForm, AddArtForm, UploadForm, ContactForm, ProfitForm, CustomerForm
from werkzeug.utils import secure_filename
from app.models import User, Art , Contact, Customer
from flask_login import login_user, logout_user, login_required, current_user
import stripe


@app.route('/')
def index():
    files = os.listdir(f"{app.config['UPLOAD_PATH']}")
    arts = Art.query.order_by(Art.art_id.desc()).all()
    user = User.query.all()

    return render_template('index.html', files=files, arts=arts, user=user)

@app.route('/thankyou/<product_id>/<user_id>', methods=['GET', 'POST'])
def thankyou(product_id, user_id):
    form = CustomerForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        country = form.country.data
        zipcode = form.zipcode.data
        email = form.email.data
        number = form.number.data
        art_id = user_id

        customer_info = Customer(first_name=first_name, last_name=last_name, address=address, city=city, state=state, country=country, zipcode=zipcode, email=email, number=number, art_id=art_id)


        flash(f"Thank you {customer_info.first_name.title()}! Your order is complete!", "success")
        return redirect(url_for('index'))

    return render_template('thankyou.html', form=form )



@app.route('/cancel')
def cancel():
    return render_template('errorpayment.html' )

@app.route('/profit', methods=['GET', 'POST'])
def profit():
    form = ProfitForm()
    if form.validate_on_submit():
        hours = form.hours.data
        hours_worth = form.hours_worth.data
        supply = form.supply.data

        your_profit = (hours * hours_worth) + supply
        flash(f'You should charge no less than {your_profit} for your artwork!', 'info')
        return redirect(url_for('addart'))

    return render_template('profit.html', form=form )

@app.route('/about', methods=['GET', 'POST'])
def about():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        number = form.number.data
        question = form.question.data
        print(name, number, question)

        check_comment = db.session.execute(db.select(Contact).filter((Contact.name == name) | (Contact.number == number))).scalars().all()
        if check_comment:

            flash("You have already reached out to us. Please give us 24 hours to respond. Thank you for your patience!", "warning")
            return redirect(url_for('about'))

        new_form = Contact(name=name, number=number, question=question)
        flash(f"Thank you {new_form.name.title()} for reaching out to us!", "success")
        return redirect(url_for('about'))

    return render_template('about.html', form=form)

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
        flash(f"Thank you {new_user.username.title()} for signing up!", "success")
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
            flash(f'You have succesfully logged in as @{username.title()}!', "success")
            return redirect(url_for('index'))
        else:
            flash(f'Invalid username or password', "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/profile/<username>')
def profile(username):

    profile = User.query.filter_by(username=username).first()
    print(profile.id)
    if profile is None:
        return redirect(url_for('signup'))
    else:
        arts = Art.query.order_by(Art.art_id.desc()).all()
        return render_template('profile.html', username=username, arts=arts, profile=profile)

@app.route('/notifications/<art_id>', methods=['GET', 'POST'])
@login_required
def notifications(art_id):
    customer_purchase = Customer.query.filter_by(art_id=art_id)
    return render_template('notifications.html', customer_purchase=customer_purchase)
    # flash("You don't have any notifications available", "info")
    # return redirect(url_for('profile', username=current_user.username))

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", 'success')
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

        flash(f"{art.title} has been created!", "success")
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

        check_art = db.session.execute(db.select(Art).filter((Art.title == title) | (Art.description == description))).scalars().all()
        if check_art:

            flash("A user with that title/description already exists", "warning")
            return redirect(url_for('addart'))

        new_art = Art(title=title, width=width, height=height, description=description, price=price, user_id=current_user.id)
        print("New artwork added")
        print(new_art.price)
        int_num = int(new_art.price)
        print({int_num})

        price_data = {
            'currency': 'usd',
            'unit_amount_decimal': str(int_num*100)
        }

        flash(f"{new_art.title} has been created!", "success")
        new_product = stripe.Product.create(name=new_art.title, description=new_art.description, default_price_data=price_data, id=new_art.art_id)

        new_art.stripe_product_id = new_product.id
        db.session.commit()

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
    flash(f"{art_to_delete.title.title()} has been deleted", "info")
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
        return redirect(url_for('upload_file', artwork_id=art_id))

    form.title.data = art_to_edit.title
    form.width.data = art_to_edit.width
    form.height.data = art_to_edit.height
    form.description.data = art_to_edit.description
    form.price.data = art_to_edit.price

    return render_template('edit.html', form=form, art=art_to_edit)

@app.route('/editinfo/<user_id>', methods=["GET", "POST"])
@login_required
def edit_info(user_id):
    form = SignUpForm()
    user_to_edit = User.query.get_or_404(user_id)
    if user_id == current_user.id:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user_to_edit.first_name = form.first_name.data
        user_to_edit.last_name = form.last_name.data
        user_to_edit.address = form.address.data
        user_to_edit.city = form.city.data
        user_to_edit.state = form.state.data
        user_to_edit.zipcode = form.zipcode.data
        user_to_edit.email = form.email.data
        user_to_edit.username = form.username.data
        user_to_edit.password = form.password.data

        db.session.commit()
        flash(f"@{user_to_edit.username.title()} has been edited!", "success")
        return redirect(url_for('index'))

    form.first_name.data = user_to_edit.first_name
    form.last_name.data = user_to_edit.last_name
    form.address.data = user_to_edit.address
    form.city.data = user_to_edit.city
    form.state.data = user_to_edit.state
    form.zipcode.data = user_to_edit.zipcode
    form.email.data = user_to_edit.email
    form.username.data = user_to_edit.username
    form.password.data = user_to_edit.password

    return render_template('editinfo.html', form=form, user_info=user_to_edit)


@app.route('/order/<product_id>/<user_id>', methods=["GET", "POST"])
def order(product_id, user_id):

    pull_art = stripe.Product.retrieve(product_id)
    price_id = pull_art.get("default_price")

    session = stripe.checkout.Session.create(
        line_items = [{
            'price': price_id,
            'quantity': 1,
        }],
        mode = 'payment',
        success_url = 'http://localhost:5000' + url_for('thankyou', product_id=product_id, user_id=user_id),
        cancel_url = 'http://localhost:5000' + url_for('cancel')

    )

    return redirect(session.url, code=303)
