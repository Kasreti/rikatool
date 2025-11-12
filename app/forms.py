from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def lengthcheck(min=1, max=255):
    message = 'Must be between %d and %d characters long.' % (min, max)
    def _lengthcheck(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)
    return _lengthcheck


class searchWord(FlaskForm):
    word = StringField('Search by word or definition:')
    submit = SubmitField('Search by Rikatisyï')
    fuzsubmit = SubmitField('Rikatisyï (Fuzzy)')
    defsubmit = SubmitField('Search by definition')
    random = SubmitField('Random word')
    refresh = SubmitField('Refresh Dictionary')
    markentry = SubmitField('Mark entry as erroneous')
    genipa = SubmitField('Generate IPA')
