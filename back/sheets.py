import pygsheets
from datetime import datetime
import pytz
import json

service_account_json = {
  "type": "service_account",
  "project_id": "rubikon-452014",
  "private_key_id": "517c8988512b607c5eeba7d2cbe45d4d30c29947",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDHCJsskq10KP5g\nqNp+rXjmwU0IzbozIqnEJnL2Fg5p5P95CK86+WovzGuplvoNVS7mrZDaA/9lIf5P\nPVeQ7CjgdnvQr3rl0w/08+UgjB3tkfBTODRO8jl8vRVmbYMeDUjd6qmsVB2jHrsM\noj4Q3JKzI410r2CQ/92ujOOlJwz0JD6HYQ/2yi5e6lCXHUOelx1zuua3vDz1pAf8\nNpz9FbJa26hpq08T6sYyJYBNq8p8kvMcj+okJ9PxTljA1feDA/IsgjTBFJiSsUz/\n/UvCoWvMO3yVgQRnnHwA9VseEYVVhZrCVwF/GE2q55wdVb1IK5OypK7ZoSXI8toU\nHw9vj7mnAgMBAAECggEAJLiyRI2FYh6kHDpbIa8o1M5KQ7sNRRz6nH2JjVyxaRk+\nh1qyVdupm0sIfCAmX2pdfmL8jDTbnJGihYUoUE06F3vUyUJvFtMTqRqMpi4j4W6h\nHAGNKRmowJp0RdMjs1o5HPSMPIbCdxOW6DRQ5jSD/ngrQ6GN3ALRKEDHSXPEgJCR\nheBSjmotcbNfydTIURx6KfUCYLRSKut99FI0neKeD8vpZQiPWgdRLLdChGFc1HCw\np2RXNhiIy2sSkEajIBLDHPuqFf8urGccNNbyKJefycUbnsMymopzyF91RljxryWr\n7diOLqvUWnhj0pDqTQVDYshL+BejGrUfJUEjwwGEMQKBgQD8dWq0mkQTvfb2nGT3\nHNYWr57xtWEPOwy9zfA4CkyqAR8TyO+wP8yzwFPOMS+G92GiCM9ellj4nKhpW1Wc\nFPw4Kn6JgaycoKNrgKgYd/ws8FmgKHCbTWhGXejX6aX5NEs1bq3iCavhTwQK/ybo\na8emSVb3N4XnL9Y/tfzKb6DBFwKBgQDJ01bRRfXSDdS3SkhL37rWohURsU5RxNhq\nzM6H7CSXdAWpc5sfvg2C5gBVHw9yQuyXOn8vb7T8rWoHlq3xPNmpxkAyq5l4SUl6\nONELoA65+couvr/HvFZPgz5bztfiIMwRQ27FxQ0AQmyw6I9gzvoBoSlpq4lIAyV6\nJY532f+F8QKBgCKA9bV7RASiuOcZlt8DLOtq00Fbtck8G9CxHby7A6FUh+fPVZr0\nDUkf5xROOp2qn8hihdz6lWxdFNNZbUjowVP30tV+SJYbilo9+jtl4qxNqSIvhLxl\nBvRfD1y7DTkTAZhq6Q70nW4su3O5TZsEaAP9EAq3pvBi5FhOyh7sxL6/AoGAVEHG\nnNd4KJldlKeORx7AAZro8Nn0uG5Va0DVeCk9nXzyYCvDNx1AxsT+noq5CBqoavog\n3szj4hkDiud89plQxW/enUjGaVEvO7c8jn3jqACAR8OajOgzoD5KakmQFvdaOlrM\nhAQfyVvxxGlScjf2Z3fAsjzKsyWdH8FOGPsJkgECgYEAgK0Nl6J8d9D/GZTOe8fd\nXjEmtPgXEaf4MgLOG1QEijXftZBDYI+qWM5+FYiBOm9lHvU8k+Goo8wM3MlJjYT/\nZAEWL/q+3wiKCturSm0K9sNMd1cpmmjeyJYMaiiaVjqqZ444NJA382b6JGZefWur\nj1TmFGpTRNZdzxsW9jBOqp4=\n-----END PRIVATE KEY-----\n",
  "client_email": "owner-496@rubikon-452014.iam.gserviceaccount.com",
  "client_id": "115253401796145067017",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/owner-496%40rubikon-452014.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


service_account_json = json.dumps(service_account_json)
client = pygsheets.authorize(service_account_json=service_account_json)

table = client.open('Новая таблица')
wks = table.worksheet_by_title('Основное')

comments = {
    '': '',
    'День рождения (10%)': 'скидка др проверить доки',
    'Администратор (10%)': 'скидка админ',
    'Отметка (5%)': 'скидка отметка'
}

tz = pytz.timezone('Asia/Irkutsk')


def correct_service(service):
    service = service.replace('Аренда зала «', '').replace('Киносвидание «', '').replace('»', '')
    if service.endswith(')'):
        rate, temp, room = service.split(' ')
        if room in ['M)', 'S)']:
            service = rate + ' (' + room
        else:
            service = rate
    return service


# def color_cells(pay: bool) -> None:
#     for address in ['G2', 'H4']:
#         wks.cell(address).color = (1, 0, 0, 1) if not pay else (1, 1, 1, 1)


def update_prepayment(values: dict) -> None:
    # service = values['service'].replace('Аренда зала «', '').replace('Киносвидание «', '').replace('»', '')
    service = correct_service(values['service'])
    date = values['not_formatted_date'].split('-')
    today = datetime.now(tz=tz).strftime('%d.%m.%Y')
    data = [today, 'Предоплата', '', '', f'{date[2]}.{date[1]} {service} {values["start"]}', '',
            values['prepayment'].replace('.', ','), values['worker']]
    wks.update_values('A2:H2', [data])


def update_reservation(values: dict) -> None:
    service = correct_service(values['service'])
    if values['service'].endswith(')'):
        service = 'Киносвидание ' + service
    date = values['not_formatted_date'].split('-')
    time = values['start'] + '-' + values['end']
    prepayment = values['prepayment'].replace('.', ',')

    data = [f'{date[2]}.{date[1]}.{date[0]}', values['name'], values['phone'], values['source'], service, time, values['clients'],
            prepayment, prepayment, values['amount'], values['worker'], comments[values['discount']]]
    wks.update_values('A4:L4', [data])
