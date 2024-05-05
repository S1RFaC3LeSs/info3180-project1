"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from app.models import Property
from app.forms import PropertyForm
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, send_from_directory


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

# Fetch all properties
@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template("properties.html", properties=properties)

@app.route('/properties/create', methods=['GET', 'POST'])
def create():
    form = PropertyForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        property_ = Property(
            title=form.title.data,
            numBedrms=form.numBedrms.data,
            numBathrms=form.numBathrms.data,
            location=form.location.data,
            price=form.price.data,
            propType=form.propType.data,
            description=form.description.data,
            photo_filename=filename
        )
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        db.session.add(property_)
        db.session.commit()
        flash("Successfully Added")
        return redirect(url_for('properties'))
    return render_template("create.html", form=form)

# Fetch a specific property by ID
@app.route('/properties/<propertyid>')
def property(propertyid):
    prop = Property.query.get_or_404(propertyid)
    return render_template('property.html', property=prop)

# Serve uploaded images
@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


###
# The functions below should be applicable to all Flask apps.
###

# Create new property


# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
