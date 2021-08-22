from django.forms import ModelForm
from django import forms

from .models import *

class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'

class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'