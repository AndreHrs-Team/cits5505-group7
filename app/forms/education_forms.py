from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import SubmitField

from wtforms import SubmitField


class AddEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Add Event')
    description = TextAreaField('Description')