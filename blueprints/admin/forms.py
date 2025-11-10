from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class IceTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    category = SelectField('Category', choices=[('block', 'Block'), ('cube', 'Cube'), ('flake', 'Flake')],
                          validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=500)])
    price_per_unit = FloatField('Price per Unit', validators=[DataRequired(), NumberRange(min=0.01)])
    unit = StringField('Unit', validators=[DataRequired(), Length(min=1, max=10)])
    in_stock = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField('Image URL', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Ice Type')

class OrderStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'), ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')

class ReportForm(FlaskForm):
    date_from = DateField('From Date', validators=[DataRequired()])
    date_to = DateField('To Date', validators=[DataRequired()])
    submit = SubmitField('Generate Report')
