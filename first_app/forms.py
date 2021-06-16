from django import forms




class StockSymbolForm(forms.Form):
    symbol = forms.CharField(max_length=6,min_length=1,strip=True,widget=forms.widgets.TextInput(
        attrs={'class': 'form-control',
               'placeholder':'GOOG'}
    ))


