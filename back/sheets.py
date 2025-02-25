import pygsheets

client = pygsheets.authorize(service_file='service_account.json')

# sh = client.create('Новая таблица')
table = client.open('Новая таблица')
wks = table.sheet1

# wks.update_value('A1', "Numbers on Stuff")
table.share('mhidt.unsaint@gmail.com', role='writer')
# print(table.url)
