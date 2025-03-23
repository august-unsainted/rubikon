import copy
from math import floor

from back.data import *


def get_hours(start: str, end: str) -> float:
    if start == '11:00' and end == '22:00':
        return 6
    start = start.replace('00:', '24:')
    end = end.replace('00:', '24:')
    if start > end:
        start = start.replace('24:', '00:')
    hours = int(end[:2]) - int(start[:2])
    minutes = int(end[3:]) - int(start[3:])
    hours = hours + minutes / 60
    return hours


def get_end(start: str, hours: str) -> str:
    if hours:
        start = start.replace('00:', '24:')
        if float(hours) % 1 != 0:
            end_hours = floor(float(hours))
            end_minutes = floor(float(hours) % 1 * 60)
            end = f'{str(end_hours).rjust(2, '0')}:{str(end_minutes).rjust(2, '0')}'
        else:
            end_hours = int((int(start[:2]) + float(hours)) % 24)
            end = f'{str(end_hours).rjust(2, '0')}:{start[3:]}'
        return end
    return '00:00'


def get_amounts(service: str, hours: str, discount: str) -> (str, str):
    amount = int(int(price[service]) * float(hours))
    if discount:
        discount = discount.split('(')[-1][:-2]
        amount -= int(amount / 100 * int(discount))
    prepayment = amount / 2
    return str(amount), str(prepayment)


def get_date(info: dict) -> str:
    date = info['date']
    if date == info['today']:
        date = 'сегодня'
    elif date == info['tomorrow']:
        date = date[:date.index(' (')]
        date = f'завтра ({date})'
    return date


def get_prepayment_info(info: dict[str, str]) -> (str, str):
    info = copy.deepcopy(info)
    info['service'] = (info['service'].replace('Аренда', 'аренды').replace('ие', 'ия'))
    amount, prepayment = ["{:,}".format(float(info[key])).replace(',', ' ').replace('.0', '')
                          for key in ['amount', 'prepayment']]
    date = f'на {get_date(info)}'
    discount = 'с учётом скидки ' if info['discount'] else ''
    template = prepayment_template
    if not info['already_was']:
        template += prepayment_addictional
    prepayment_text = template.format(info['service'], date, info['start'], info['end'], discount, amount,
                                                 prepayment)
    return prepayment_text


def get_results(info: dict) -> dict:
    hours = floor(float(info['hours']))
    minutes = floor(float(info['hours']) % 1 * 60)
    for key in result_fields:
        if key == 'time':
            minutes = '' if not minutes else f" {minutes}м"
            result = f'с {info['start']} до {info['end']} ({hours}ч{minutes})'
        elif key == 'discount':
            result = info['discount'] if info['discount'] else 'Без скидки'
        elif key in ['amount', 'prepayment']:
            result = "{:,} рублей".format(float(info[key])).replace(',', ' ').replace('.0', '')
        else:
            result = info[key]
        info['summary-' + key] = result
    return info


def get_main_info(values: dict) -> dict:
    info = {}
    for key in fields:
        if key in ['start', 'end']:
            info[key] = f'{values[key + '-hour']}:{values[key + '-minute']}'
        else:
            info[key] = values[key]

    start, end, hours = info['start'], info['end'], info['hours']

    if (start and end) or (start and hours):
        if info['service'].startswith('Киносвидание') and info['discount'] == 'День рождения (10%)':
            info['discount'] = ''

        info['amount'], info['prepayment'] = get_amounts(info['service'], info['hours'], info['discount'])

        get_results(info)
        return info
    return


def get_addictional_info(info: dict) -> dict:
    start, end, hours = info['start'], info['end'], info['hours']

    if (start and end) or (start and hours):
        info['prepayment_info'] = get_prepayment_info(info)

        flag = not [key for key in fields if not info[key] and key != 'discount']

        if flag:
            reminder = ('Пожалуйста, не забудьте взять с собой оригинал свидетельства о рождении или '
                        'паспорта для подтверждения скидки)\n\n')
            template = goodbye_short_template if info['already_was'] else goodbye_template

            goodbye = template.format(get_date(info), info['start'],
                                              reminder if info['discount'] == 'День рождения (10%)' else '')
            info['goodbye_info'] = goodbye
    return info
