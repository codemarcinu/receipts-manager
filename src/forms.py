from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DecimalField, DateField
from wtforms.validators import DataRequired, Optional

class ReceiptUploadForm(FlaskForm):
    receipt_image = FileField('Receipt Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    store = StringField('Store Name', validators=[Optional()])
    purchase_date = DateField('Purchase Date', validators=[Optional()])
    total_amount = DecimalField('Total Amount', validators=[Optional()])

class ReceiptVerificationForm(FlaskForm):
    store = StringField('Store Name', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    total_amount = DecimalField('Total Amount', validators=[DataRequired()])
