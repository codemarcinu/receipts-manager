from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DecimalField, DateField, SelectField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from datetime import date

class ProductForm(FlaskForm):
    """Formularz dla pojedynczego produktu z paragonu."""
    id = HiddenField('ID')
    name = StringField(
        'Nazwa produktu',
        validators=[
            DataRequired(message='Nazwa produktu jest wymagana'),
            Length(min=2, max=200, message='Nazwa produktu musi mieć od 2 do 200 znaków')
        ]
    )
    unit_price = DecimalField(
        'Cena jednostkowa',
        validators=[
            DataRequired(message='Cena jest wymagana'),
            NumberRange(min=0, message='Cena musi być większa od 0')
        ],
        places=2
    )
    quantity = DecimalField(
        'Ilość',
        validators=[
            DataRequired(message='Ilość jest wymagana'),
            NumberRange(min=0, message='Ilość musi być większa od 0')
        ],
        places=3
    )
    unit = StringField(
        'Jednostka',
        validators=[Optional(), Length(max=20)]
    )
    category_id = SelectField(
        'Kategoria',
        validators=[Optional()],
        coerce=int,
        choices=[]
    )
    expiry_date = DateField(
        'Data ważności',
        validators=[Optional()]
    )

    class Meta:
        csrf = False

class ReceiptVerificationForm(FlaskForm):
    """Formularz do weryfikacji danych z paragonu."""
    receipt_id = HiddenField('ID Paragonu')
    store_name = StringField(
        'Nazwa sklepu',
        validators=[
            DataRequired(message='Nazwa sklepu jest wymagana'),
            Length(min=2, max=200, message='Nazwa sklepu musi mieć od 2 do 200 znaków')
        ]
    )
    purchase_date = DateField(
        'Data zakupu',
        validators=[DataRequired(message='Data zakupu jest wymagana')]
    )
    total_amount = DecimalField(
        'Suma',
        validators=[
            DataRequired(message='Suma jest wymagana'),
            NumberRange(min=0, message='Suma musi być większa od 0')
        ],
        places=2
    )
    products = FieldList(FormField(ProductForm), min_entries=1)

    def __init__(self, *args, categories=None, **kwargs):
        super().__init__(*args, **kwargs)
        if categories:
            choices = [(0, '-- Wybierz kategorię --')] + [(c.id, c.name) for c in categories]
            for product_form in self.products:
                product_form.category_id.choices = choices

class ReceiptUploadForm(FlaskForm):
    """Formularz do uploadu nowego paragonu."""
    store_name = StringField(
        'Nazwa sklepu',
        validators=[
            DataRequired(message='Nazwa sklepu jest wymagana'),
            Length(min=2, max=200, message='Nazwa sklepu musi mieć od 2 do 200 znaków')
        ]
    )
    
    purchase_date = DateField(
        'Data zakupu',
        validators=[DataRequired(message='Data zakupu jest wymagana')],
        default=date.today
    )
    
    receipt_image = FileField(
        'Zdjęcie paragonu',
        validators=[
            FileRequired(message='Plik jest wymagany'),
            FileAllowed(['jpg', 'jpeg', 'png'], message='Dozwolone są tylko pliki obrazów (jpg, jpeg, png)')
        ]
    )