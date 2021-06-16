from django import forms
import requests



class StockSymbolForm(forms.Form):
    symbol = forms.CharField(max_length=4,min_length=4,strip=True,widget=forms.widgets.TextInput(
        attrs={'class': 'form-control',
               'placeholder':'GOOG'}
    ))


