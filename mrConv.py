import telebot
from config import keys, TOKEN
from extensions import ConvertionException, MrConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = f"Доброго времени суток, {message.chat.username}!\n"\
           'Для начала работы с ботом необходимо ввести через пробел:\n'\
           '<имя валюты, цену которой Вы хотите узнать> далее,\n'\
           '<имя валюты, в которую надо перевести первую>\n'\
           '<количество первой валюты>.\n'\
           'Увидеть список достпных для конвертации валют, можно использовав команду: /values'
    bot.reply_to(message,text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message,text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Недопустимое количество параметров.')

        quote, base, amount = values
        total_base = MrConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Вы ошиблись.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Меня на такое не программировали.\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base}, составляет {total_base}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['voice'])
def voise_messege(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'У Вас восхитительный голос, но для того, чтобы получить результат, нужно печатать ручками с клавиатуры.\n'
                                      'Более подробная информация по запросу команды </help>.')


@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    bot.send_message(message.chat.id, 'Очень любопытно, но я предпочитаю обсуждать курсы валют.\n'
                                      'Более подробная информация по запросу команды </help>.')




bot.polling()
