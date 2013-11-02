from models import Transaction,Transaction_final,Ticket
from django import forms

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket

class EditTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['cost','ticket_show','ticket_is_discounted']

class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction