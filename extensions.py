import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class MrConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException('Введены одинаковые валюты. Это не имеет смысла.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException('Недопустимое название валюты.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException('Недопустимое название валюты.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Недопустимая сумма валюты.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
