checkbox_texts = [
    'Отправил клиенту все сообщения',
    'Записал предоплату в таблицу',
    'Записал бронь в “Брони”',
    'Добавил бронь в DIKIDI'
]

result_fields = ['service', 'amount', 'prepayment', 'date', 'time', 'discount']

price = {
    'Киносвидание «Lite» (зал XS)': 300, 'Киносвидание «Middle» (зал S)': 600, 'Киносвидание «Middle» (зал M)': 600,
    'Киносвидание «Max» (зал L)': 900,
    'Аренда зала «XS»': 500, 'Аренда зала «S»': 1000, 'Аренда зала «M»': 1000, 'Аренда зала «L»': 1250, 'Аренда зала «XL»': 1500
}

fields = ['name', 'date', 'phone', 'start', 'service', 'end', 'clients', 'hours', 'discount', 'not_formatted_date',
          'today', 'tomorrow', 'already_was']

prepayment_template = (
    "Бронируем мы по 50% предоплате ☺️\n\n"
    "Стоимость {} {} c {} до {} {}составила:\n"
    "— {} рублей\n\n"
    "Предоплата:\n"
    "— {} рублей\n\n"
    "РЕКВИЗИТЫ:\n"
    "❗️СБЕРБАНК - 89085995085\n"
    "Получатель Павел Львович Л.\n\n"
    "Как переведете, пожалуйста, отправьте сюда чек или скриншот)"
)

prepayment_addictional = (
    "\n\n❗️ Место закрепляется за Вами сразу же после внесения предоплаты 🙌🏽\n\n"
    "При отмене события предоплата возвращается не позже, чем за 2 суток. Если Вы отменяете бронь менее, чем за "
    "2 суток, она будет конвертирована в Ваш депозит на соответствующую сумму, который в дальнейшем Вы сможете "
    "потратить в нашем заведении.\n\n"
    "После внесения предоплаты, отправьте, пожалуйста, Ваше имя и номер для связи ☺️"
)

# goodbye_template = ('Отлично! Будем ждать вас {} в {})\n\n'
#                     '{}'
#                     'С собой можете взять сменную обувь, но у нас есть тапочки, если что ☺️\n\n'
#                     'Адрес: Хоца Намсараева, 2в\n'
#                     'До встречи! ❤️')

goodbye_template = ('Отлично! Будем ждать вас {} в {})\n'
                    '{}'
                    '{}'
                    'До встречи! ❤️')
