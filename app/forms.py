from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField, SelectField
from flask_wtf.file import FileAllowed, FileRequired, FileField

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    numBedrms = StringField('Number of Bedrooms', validators=[InputRequired()])
    numBathrms = StringField('Number of Bathrooms', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    propType = SelectField(u'Property Type',
    choices=[('apartment', 'Apartment'),
    ('house', 'House')])
    description = StringField('Description', validators=[InputRequired()])
    photo = FileField('Photo', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png'], 'Images only!')])