import requests
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import StockSymbolForm

from django.shortcuts import render

from django.core.exceptions import FieldError
from zeep import Client
from zeep import xsd

import datetime
from .models import ApiKeys


class HomeView(TemplateView, FormView):
    template_name = 'first_app/home.html'
    form_class = StockSymbolForm

    def get(self, request, *args, **kwargs):
        if request.GET.get('symbol') is None:
            return render(request, self.template_name, {'form': self.get_form(), 'initial': True})
        else:
            symbol = request.GET.get('symbol')
            data = self.fetch_data(symbol)
            if data['Outcome'] == 'RegistrationError':
                raise FieldError('Api Error')
            elif data['Outcome'] == 'RequestError':
                raise FieldError('Invalid Input')
            else:
                return render(request, self.template_name, {'form': self.get_form(), 'data': data})

    def get_data(self, symbol1):
        symbol = 'AAPL'  # form.cleaned_data['symbol']
        header = xsd.Element(
            '{http://www.xignite.com/services/}Header',
            xsd.ComplexType([
                xsd.Element(
                    '{http://www.xignite.com/services/}Username',
                    xsd.String()
                )
            ])
        )

        header_value = header(Username='7141A17000624B71AD5096397A28B6B7')

        parameters = {
            'Identifier': symbol,
            'IdentifierType': 'Symbol',
            'IdentifierAsOfDate': '6/15/2021',
            'AdjustmentMethod': 'All',
            'EndDate': '6/14/2021',
            'PeriodType': 'Year',
            'Periods': '1'
        }

        client = Client('http://globalhistorical.xignite.com/v3/xGlobalHistorical.asmx?WSDL')
        result = client.service.GetGlobalHistoricalQuotesTrailing(**parameters, _soapheaders=[header_value])

        # A real application should include some error handling. This example just prints the response.
        print(result)
        return result

    def fetch_data(self, symbol):
        obj = ApiKeys.objects.filter(active=True).get()
        key=obj.non_enc_key
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        url = f"https://globalhistorical.xignite.com/v3/xGlobalHistorical.json/GetGlobalHistoricalQuotesTrailing?IdentifierType=Symbol&Identifier={symbol}&IdentifierAsOfDate={today}&AdjustmentMethod=All&EndDate={today}&PeriodType=Month&Periods=1&_token={key}"
        r = requests.get(url)
        return r.json()



