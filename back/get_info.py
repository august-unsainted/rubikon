import copy
from datetime import datetime

from back.data import *


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
    if hours:
        start = start.replace('00:', '24:')
        end_hours = (int(start[:2]) + int(hours)) % 24
        end = f'{str(end_hours).rjust(2, '0')}:{start[3:]}'
        return end
    return '00:00'


def get_amounts(service: str, hours: str, discount: str) -> (str, str):
    amount = int(price[service]) * int(hours)
    if discount:
        discount = discount.split('(')[-1][:-2]
        amount -= int(amount / 100 * int(discount))
    return str(amount), str(amount / 2)[:-2]


def get_prepayment_info(info: dict[str, str]) -> (str, str):
    info = copy.deepcopy(info)
    info['service'] = (info['service'].replace('Аренда', 'аренды').replace('ие', 'ия'))
    amount, prepayment = ["{:,}".format(int(info[key])).replace(',', ' ')
                          for key in ['amount', 'prepayment']]
    date = f'на {info['date']} ' if info['date'] else ''
    discount = 'с учётом скидки ' if info['discount'] else ''
    prepayment_text = prepayment_template.format(info['service'], date, info['start'], info['end'], discount, amount,
                                                 prepayment)
    return prepayment_text


def get_results(info: dict) -> dict:
    for key in result_fields:
        if key == 'time':
            result = f'с {info['start']} до {info['end']} ({info['hours']}ч)'
        elif key == 'discount':
            result = info['discount'] if info['discount'] else 'Без скидки'
        elif key in ['amount', 'prepayment']:
            result = "{:,} рублей".format(int(info[key])).replace(',', ' ')
        else:
            result = info[key]
        info['summary-' + key] = result
    return info


def get_main_info(values: dict) -> dict[str: str]:
    info = {}
    for key in fields:
        if key in ['start', 'end']:
            info[key] = f'{values[key + '-hour']}:{values[key + '-minute']}'
        else:
            info[key] = values[key]

    start, end, hours = info['start'], info['end'], info['hours']

    if (start and end) or (start and hours):
        if hours:
            info['end'] = get_end(start, hours)
        else:
            info['hours'] = get_hours(start, end)

        if info['service'].startswith('Киносвидание') and info['discount'] == 'День рождения (10%)':
            info['discount'] = ''

        info['amount'], info['prepayment'] = get_amounts(info['service'], info['hours'], info['discount'])
        info['prepayment_info'] = get_prepayment_info(info)

        get_results(info)

        flag = not [key for key in fields if not info[key] and key != 'discount']

        if flag:
            reminder = ('Пожалуйста, не забудьте взять с собой оригинал свидетельства о рождении или '
                        'паспорта для подтверждения скидки)\n\n')

            goodbye = goodbye_template.format(info['date'], info['start'],
                                              reminder if info['discount'] == 'День рождения (10%)' else '')
            info['goodbye_info'] = goodbye
        return info
    return


# def set_hours_of_work(date: str) -> list:
#     weekday = datetime.strptime(date, '%Y.%d.%m').weekday()
#     if 0 <= weekday <= 2:
#         return [17, 0]
#     else:
#
