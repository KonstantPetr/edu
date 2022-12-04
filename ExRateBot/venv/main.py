import telebot
import requests
import json
from extensions import *

with open('token.json') as token_cfg:
    TOKEN = json.load(token_cfg)['bot_token']

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Приветствую, {message.chat.username}.\n'
                                      f'Я могу помочь тебе с переводом валют!\n'
                                      f'Просто напиши запрос с виде: eur rub 100 и получишь результат!\n'
                                      f'Используй /help если что-то не понял.\n'
                                      f'Используй /values чтобы увидеть полный список доступных валют.')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, f'Формат ввода:\n'
                                      f'a b c, где:\n'
                                      f'a - валюта, цену которой надо узнать\n'
                                      f'b - валюта, в которой надо узнать цену\n'
                                      f'с - количество целевой валюты (a)\n'
                                      f'Например, требуется узнать сколько рублей стоит 10 евро.\n'
                                      f'Тогда пишем: eur rub 10\n'
                                      f'Список доступных валют можно увидеть с помощью команды /values')


@bot.message_handler(commands=['values'])
def send_values(message):
    currencies = get_available_values()
    cur_list = 'Код            Название валюты\n'
    i = 0
    for cur_abbr in currencies:
        i += 1
        cur_list += f'{str(cur_abbr).ljust(15)} {currencies[cur_abbr]}\n'
        if (len(cur_list) > 3000) or (i == len(currencies)):
            bot.send_message(message.chat.id, f"{cur_list}")
            cur_list = ''


@bot.message_handler(commands=['ShowMeFoxy'])
def foxy(message):
    r = requests.get('https://randomfox.ca/floof/')
    foxy_api = json.loads(r.content)
    bot.send_photo(message.chat.id, photo=foxy_api['image'])


@bot.message_handler(content_types=['text'])
def convert_response(message):

    try:
        user_req = message.text.lower().split()
        check_request(user_req)
        base = user_req[0]
        quote = user_req[1]
        amount = user_req[2]
        check_base(base)
        check_quote(quote)
        check_equal(user_req)
        check_amount(amount)
        amount = amount_converter(amount)

    except (RequestException, BaseValueException, QuoteValueException, BaseEqualQuoteValueException,
            AmountTypeException, AmountZeroException, AmountNegativeException) as e:
        price = e

    else:
        price = CurConvRequest.get_price(base, quote, amount)

    finally:
        bot.send_message(message.chat.id, f"{price}")


bot.polling(none_stop=True)
