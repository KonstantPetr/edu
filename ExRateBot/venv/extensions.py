import requests
import json


class CurConvRequest:

    @staticmethod
    def get_price(base: str, quote: str, amount: (int, float)):
        request_map = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/' \
                      f'{base}/{quote}.json'
        r = requests.get(request_map)
        text = json.loads(r.content)
        return round(amount * text[quote], 2)


class APIException(Exception):
    pass


class RequestException(APIException):
    def __str__(self):
        return 'Вы ввели что-то не то, правильный вид запроса можно увидеть с помощью команды /help'


class ValueException(APIException):
    pass


class AmountException(APIException):
    pass


class BaseValueException(ValueException):
    def __str__(self):
        return 'Вы ввели несуществующую валюту для конвертации, ' \
               'список доступных валют можно увидеть с помощью команды /values'


class QuoteValueException(ValueException):
    def __str__(self):
        return 'Вы ввели несуществующую валюту, в которую производится конвертация, ' \
               'список доступных валют можно увидеть с помощью команды /values'


class BaseEqualQuoteValueException(ValueException):
    def __str__(self):
        return 'Нельзя конвертировать валюту в ту же валюту, конвертируйте разные валюты друг в друга!'


class AmountTypeException(AmountException):
    def __str__(self):
        return 'Количество валюты должно быть целым или вещественным числом!'


class AmountZeroException(AmountException):
    def __str__(self):
        return 'Количество валюты не может быть нулевым!'


class AmountNegativeException(AmountException):
    def __str__(self):
        return 'Количество валюты не может быть отрицательным!'


def check_request(user_request):
    if len(user_request) != 3:
        raise RequestException


def check_base(base):
    if base not in get_available_values():
        raise BaseValueException


def check_quote(quote):
    if quote not in get_available_values():
        raise QuoteValueException


def check_equal(user_request):
    if user_request[0] == user_request[1]:
        raise BaseEqualQuoteValueException


def check_amount(amount):
    amount = little_secret(amount)
    try:
        float(amount)
    except ValueError:
        raise AmountTypeException

    if float(amount) == 0:
        raise AmountZeroException

    if float(amount) < 0:
        raise AmountNegativeException


def get_available_values():
    r = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json')
    return json.loads(r.content)


def little_secret(amount):
    if amount.find(',') != -1:
        return amount.replace(',', '.')
    else:
        return amount


def amount_converter(amount):
    amount = little_secret(amount)
    try:
        return int(amount)
    except ValueError:
        return float(amount)
