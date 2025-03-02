import pygsheets
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Irkutsk')

client = pygsheets.authorize(service_account_file='D:/Trash/rubikon/service_account.json')

table = client.open('Новая таблица')
wks = table.worksheet_by_title('Основное')

comments = {
    '': '',
    'День рождения (10%)': 'скидка др проверить доки',
    'Администратор (10%)': 'скидка админ',
    'Отметка (5%)': 'скидка отметка'
}
# wks.update_values('A1:K1', [["01.01.2025"], ['L'], [2], [False], ["17:00"], ["18:00"], ['900'], [], [], [], ['скидка др'
# ]], majordim='COLUMNS')


def correct_service(service):
    service = service.replace('Аренда зала «', '').replace('Киносвидание «', '').replace('»', '')
    if service.endswith(')'):
        rate, temp, room = service.split(' ')
        if room in ['M)', 'S)']:
            service = rate + ' (' + room
        else:
            service = rate
    return service


def color_cells(pay: bool) -> None:
    for address in ['G2', 'H4']:
        wks.cell(address).color = (1, 0, 0, 1) if not pay else (1, 1, 1, 1)


def update_prepayment(values: dict) -> None:
    # service = values['service'].replace('Аренда зала «', '').replace('Киносвидание «', '').replace('»', '')
    service = correct_service(values['service'])
    date = values['not_formatted_date'].split('-')
    today = datetime.now(tz=tz).strftime('%d.%m.%Y')
    data = [today, 'Предоплата', '', '', f'{date[2]}.{date[1]} {service} {values["start"]}', '',
            values['prepayment'], values['worker']]
    wks.update_values('A2:H2', [data])


def update_reservation(values: dict) -> None:
    service = correct_service(values['service'])
    date = values['not_formatted_date'].split('-')
    time = values['start'] + '-' + values['end']

    data = [f'{date[2]}.{date[1]}.{date[0]}', values['name'], values['phone'], '', service, time, values['clients'],
            values['prepayment'], values['prepayment'], values['amount'], values['worker'], comments[values['discount']]]
    wks.update_values('A4:L4', [data])


# update_prepayment({'service': 'Киносвидание «Middle»', 'prepayment': 1800, 'date': '2025-02-27', 'start': '17:00'})
