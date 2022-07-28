import financials
import datetime

f = open('financials.csv', 'w+')
f.close()
financials.main('add', [datetime.datetime.today(), 'Donor 1', 1000])
financials.main('add', [datetime.datetime.today(), 'Donor 2', 100])
financials.main('add', [datetime.datetime(2001, 1, 12), 'Donor 3', 200])
financials.main('add', [datetime.datetime(2001, 1, 12), 'Donor 5', 300])

print(financials.main('total', [datetime.datetime(2001, 1, 12)]))