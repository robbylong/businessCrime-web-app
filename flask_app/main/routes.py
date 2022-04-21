import os
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_app import photos, db
from flask_app.main.forms import ProfileForm, Update_ProfileForm
from flask_app.models import Profile, Region
from flask_app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    file_list = []
    file_dir = "static/images/boroughpic/"
    for root, dirs, files in os.walk(file_dir):
        file_list = files
    file_list2 = []
    for f in file_list:
        file_list2.append(f.replace(".jpeg", ""))
    return render_template('index.html', title='Home page', file_list=file_list2)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('main.update_profile'))
    else:
        return redirect(url_for('main.create_profile'))


@main_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    form.region_id.choices = [(r.id, r.region) for r in Region.query.order_by('region')]
    # print(len(form.region_id.choices))
    if request.method == 'POST' and form.validate_on_submit():
        filename = None  # Set the filename for the photo to None, this is the default if the user hasn't chosen to
        # add a profile photo
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                # Save the photo using the global variable photos to get the location to save to
                filename = photos.save(request.files['photo'])
        p = Profile(username=form.username.data, region_id=form.region_id.data, photo=filename,
                    description=form.description.data, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.display_profiles', username=p.username))
    return render_template('profile.html', form=form)


@main_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter_by(
        id=current_user.id).first()  # Find the existing profile for this user
    form = Update_ProfileForm(
        obj=profile)
    form.region_id.choices = [(r.id, r.region) for r in Region.query.order_by('region')]
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            profile.photo = filename  # Update the photo field
        # profile.area = form.area.data  # Update the country field
        # profile.bio = form.bio.data  # Update the bio field
        profile.username = form.username.data  # Update the user field
        profile.region_id = form.region_id.data  # Update the region id
        profile.description = form.description.data  # Updates the description field
        try:
            db.session.commit()  # Save the changes to the database
        except:
            # redirect to home page when the username does not match the login username
            return redirect('/')
        return redirect(url_for('main.display_profiles', username=profile.username))
    return render_template('update_profile.html', form=form, photo_filename=profile.photo)


@main_bp.route('/display_profiles', methods=['POST', 'GET'], defaults={'username': None})
@main_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("main.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("Username not found.")
        return redirect(url_for("main.index"))
    filenames = []
    for result in results:
        if result.photo:
            filename = result.photo
            filenames.append(filename)
    return render_template('display_profile.html', profiles=zip(results, filenames))
