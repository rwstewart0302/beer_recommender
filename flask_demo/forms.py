from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class BeerRatings(FlaskForm):
    dogfish_head_rating = FloatField('Dogfish Head 90 Minute IPA',
                                     validators=[DataRequired()])
    old_ras_rating = FloatField('Old Rasputin Russian Imperial Stout',
                                validators=[DataRequired()])
    sn_cel_rating = FloatField('Sierra Nevada Celebration Ale',
                               validators=[DataRequired()])
    two_heart_rating = FloatField('Bell\'s Two Hearted Ale',
                                  validators=[DataRequired()])
    stone_ruin_rating = FloatField('Stone Ruination IPA',
                                   validators=[DataRequired()])
    arr_bast_rating = FloatField('Arrogant Bastard Ale',
                                 validators=[DataRequired()])
    sn_pale_rating = FloatField('Sierra Nevada Pale Ale',
                                validators=[DataRequired()])
    stone_ipa_rating = FloatField('Stone IPA',
                                  validators=[DataRequired()])
    pliny_rating = FloatField('Russian River: Pliny the Elder',
                              validators=[DataRequired()])
    founders_rating = FloatField('Founder\'s Breakfast Stout',
                                 validators=[DataRequired()])

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
