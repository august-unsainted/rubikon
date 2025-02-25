from datetime import datetime
import copy

from back.data import ButtonsData, TabsData


def get_hours(start: str, end: str) -> int:
    if start == '11:00' and end == '22:00':
        return 6
    start = start.replace('00:', '24:')
    end = end.replace('00:', '24:')
    if start > end:
        start = start.replace('24:', '00:')
    hours = int(end[:2]) - int(start[:2])
    return hours


def get_end(start: str, hours: str) -> str:
    start = start.replace('00:', '24:')
    end_hours = (int(start[:2]) + int(hours)) % 24
    end = f'{str(end_hours).rjust(2, '0')}:{start[3:]}'
    return end


def get_amounts(service: str, hours: str, discount: str) -> (str, str):
    amount = int(ButtonsData.price[service]) * int(hours)
    if discount:
        discount = discount.split(' ')[-1]
        amount -= int(amount / 100 * int(discount))
    return str(amount), str(amount / 2)[:-2]


def get_prepayment_info(win: dict[str, str]) -> (str, str):
    win = copy.deepcopy(win)

    if win['service'].startswith('Аренда'):
        win['service'] = win['service'].replace('А', 'а').replace('аренда', 'аренды')
    else:
        win['service'] = win['service'].replace('ие', 'ия')

    amount, prepayment = ["{:,}".format(int(win[key])).replace(',', ' ') for key in ['amount', 'prepayment']]

    reservation_text = (
        f"Бронируем мы по 50% предоплате ☺️\n\n"
        f"Стоимость {win['service']} {f'на {win['date']} ' if win['date'] else ''}c {win['start']} до {win['end']} {'с учётом скидки ' if win['discount'] else ''}составила:\n"
        f"— {amount} рублей\n\n"
        f"Предоплата:\n"
        f"— {prepayment} рублей\n\n"
        f"РЕКВИЗИТЫ:\n"
        f"❗️СБЕРБАНК - 89085995085\n"
        f"Получатель Павел Львович Л.\n\n"
        f"Как переведете, пожалуйста, отправьте сюда чек или скриншот)\n\n"
        f"❗️ Место закрепляется за Вами сразу же после внесения предоплаты 🙌🏽\n\n"
        f"При отмене события предоплата возвращается не позже, чем за 2 суток. Если Вы отменяете бронь менее, чем за 2 суток, она будет конвертирована в Ваш депозит на соответствующую сумму, который в дальнейшем Вы сможете потратить в нашем заведении.\n\n"
        f"После внесения предоплаты, отправьте, пожалуйста, Ваше имя и номер для связи ☺️"
    )
    return reservation_text


def get_main_info(values: dict) -> dict[str: str]:
    win = {}
    for key in ButtonsData.buttons_texts.values():
        if key in ['start', 'end']:
            win[key] = f'{values[key + '-hour']}:{values[key + '-minute']}'
        else:
            win[key] = values[key]

    start, end, hours = win['start'], win['end'], win['hours']

    if (start and end) or (start and hours):
        if win['hours']:
            win['end'] = get_end(win['start'], win['hours'])
        else:
            win['hours'] = get_hours(win['start'], win['end'])

        if win['service'].startswith('Киносвидание') and win['discount'] == 'День рождения 10':
            win['discount'] = ''

        win['amount'], win['prepayment'] = get_amounts(win['service'], win['hours'],
                                                       win['discount'])
        win['prepayment_info'] = get_prepayment_info(win)

        for data in TabsData.keys:
            if win.get(data):
                new_data = win[data]
            elif data == 'time':
                new_data = f'c {win['start']} до {win['end']} ({win['hours']}ч)'
            else:
                continue
            win[f'gen_{data}'] = new_data

        flag = True
        for key in ButtonsData.buttons_texts.values():
            if not win[key]:
                flag = False
        if flag:
            date = datetime.strptime(win['date'], '%B, %d (%A)').strftime('%d.%m')
            short_service = win['service'].replace('Киносвидание «', '').replace('Аренда зала «', '').replace('»', '')
            table_prepayment = f'Предоплата;;{date} {short_service} {win['start']};;р.{win['prepayment']},00;;;;;Перевод'
            win['table_prepayment'] = table_prepayment
            table_reservation = (f'{win['name']};{win['phone']};;{short_service};{win['start']}-{win['end']};'
                                 f'{win['clients']};{win['prepayment']};{win['prepayment']};{win['amount']};;'
                                 f'{'скидка др проверить доки' if win['discount'][0] == 'Д' else ''}')
            win['table_reservation'] = table_reservation
            goodbye = (f'Отлично! Будем ждать вас {win['formatted_date']} в {win['start']})\n\n'
                       f'С собой можете взять сменную обувь, но у нас есть тапочки, если что ☺️\n\n'
                       f'Адрес: Хоца Намсараева, 2в\n'
                       f'До встречи! ❤️')
            win['goodbye'] = goodbye
        return win
    return


def convert_info(reservation: str) -> str:
    reservations = reservation.split('\n')
    entry = ''
    for reservation in reservations:
        data = reservation.split('	')
        date, room, time, clients, postpayment = data[0], data[4], data[5], data[6], data[8]
        comment = data[11] if len(data) == 12 else ''

        # вс, 16 февраля	Оюна	89146318777	Звонки	M	14:00-16:00	6	р.900,00	р.900,00	р.1 800,00	Рома	скидка др проверить доки
        # date, name, phone, source, room, time, clients, prepayment, postpayment, amount, admin, comment = reservation.split('	')
        time = time.split('-')
        date = date.replace('я', 'ь').replace('маь', 'мая').replace('та', '').rstrip()
        date = datetime.strptime(date, '%a, %d %B')
        year = datetime.today().year
        date = date.strftime(f'%d.%m.{year}')
        entry += f'{date};{room};{clients};{time[0]};{time[1]};{postpayment};;;;;{'скидка др' if comment == 'скидка др проверить доки' else comment}\n'
    return entry
