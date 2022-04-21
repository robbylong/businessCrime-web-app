from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from flask_app import photos
from flask_app.models import Profile
from flask_wtf.file import FileField, FileAllowed


class ProfileForm(FlaskForm):
    """ Class for the profile form """

    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    description = TextAreaField(label='Personal description', description='Write something about yourself')
    region_id = SelectField(label='Select your region', coerce=int)
    photo = FileField('Profile picture',
                      validators=[FileAllowed(photos, 'Images only!'), DataRequired(message='Image is required')])

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile is not None:
            raise ValidationError('Username already exists, please choose another username')


class Update_ProfileForm(FlaskForm):
    """ Class for the updating profile form """

    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    description = TextAreaField(label='Personal description', description='Write something about yourself')
    region_id = SelectField(label='Select your region', coerce=int)
    photo = FileField('Profile picture',
                      validators=[FileAllowed(photos, 'Images only!'), DataRequired(message='Image is required')])
