from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SelectField, FloatField, TextAreaField, DateTimeField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from datetime import datetime


class AccountForm(FlaskForm):
    """Form for managing financial accounts"""
    id = HiddenField('ID')
    name = StringField('Account Name', validators=[
        DataRequired(),
        Length(max=100, message='Account name must be less than 100 characters')
    ])
    type = SelectField('Account Type', choices=[
        ('', 'Select Type'),
        ('bank', 'Bank Account'),
        ('wallet', 'Wallet'),
        ('credit', 'Credit Card'),
        ('savings', 'Savings Account'),
        ('cash', 'Cash'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    balance = FloatField('Initial Balance', validators=[
        DataRequired(),
        NumberRange(min=0, message='Balance cannot be negative')
    ])
    note = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Account')


class CategoryForm(FlaskForm):
    """Form for managing expense/income categories"""
    id = HiddenField('ID')
    name = StringField('Category Name', validators=[
        DataRequired(),
        Length(max=100, message='Category name must be less than 100 characters')
    ])
    type = SelectField('Category Type', choices=[
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income')
    ], validators=[DataRequired()])
    icon = StringField('Icon', validators=[Optional(), Length(max=100)])
    is_global = BooleanField('Global Category')
    submit = SubmitField('Save Category')


class TransactionForm(FlaskForm):
    """Form for managing financial transactions"""
    id = HiddenField('ID')
    type = SelectField('Transaction Type', choices=[
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income')
    ], validators=[DataRequired()])
    account_id = SelectField('Account', coerce=int,
                             validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int,
                              validators=[DataRequired()])
    amount = FloatField('Amount', default=0, validators=[
        DataRequired(),
        NumberRange(min=0.00, message='Amount must not be negative'),
    ])
    date = DateTimeField('Date', format='%Y-%m-%dT%H:%M',  # Changed format
                         validators=[DataRequired()],
                         default=datetime.now().strftime('%Y-%m-%dT%H:%M'))
    title = StringField('Title', validators=[
        Optional(),
        Length(max=255, message='Title must be less than 255 characters')
    ])
    note = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Transaction')

    def __init__(self, *args, **kwargs):
        """Initialize form with dynamic account and category choices"""
        super(TransactionForm, self).__init__(*args, **kwargs)
        if 'accounts' in kwargs:
            self.account_id.choices = [
                (account.id, account.name) for account in kwargs['accounts']
            ]
        if 'categories' in kwargs:
            self.category_id.choices = [
                (category.id, category.name) for category in kwargs['categories']
            ]
