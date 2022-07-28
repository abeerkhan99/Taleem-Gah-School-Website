import csv
import datetime
"""

Structure = 

.csv
{Entry : Date (MMYY): [[Donor 1, Amount] /n [Donor 2, Amount] /n [Donor 3, Amount] .. etc]}
Identifier + Date:
-Balance Sheet

Identifier + Date: .. etc

Using this structure, every month we generate a report of all the donors and their fees paid.
Get the universal time first, if date exists already, allow update, else create a new month.

Store a month entry in 1 line of csv, keep it sorted. Final balances are cumulative so editing it changes all.
Sort by date first, then calculate the balance.

Functions= 
get_balanceSheet(date)
add_balance(date, donor, amount)
update_balance(date, donor1, amount1, donor2, amount2)
get_total(date)

"""

# update so it works sequentially and also actually uses csvs, and also auto updates

def read_csv(financial_data, path):

    data = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                data.append(row)
    # print(data)
    for i in range(len(data)):
        if data[i][0][0:7] == 'Entry: ':
            date = data[i][0][7:]
            financial_data[date] = []
            for j in range(i+1, len(data)):
                if data[j][0][0:7] != 'Entry: ':
                    financial_data[date].append([data[j][0], int(data[j][1])])
                else:
                    break

    return financial_data


def write_csv(financial_data, path):

    with open(path, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in financial_data.items():
            writer.writerow(['Entry: ' + key])
            for i in value:
                writer.writerow([i[0], i[1]])

#unchecked
def get_balanceSheet(financial_data, date):

    date = date.strftime('%Y-%m')

    if date in financial_data:
        return financial_data[date]
    else:
        return -1


def add_balance(financial_data, date, donor, amount):

    date = date.strftime('%Y-%m')
  
    if date in financial_data:
        financial_data[date].append([donor, amount])
    else:
        financial_data[date] = [[donor, amount]]
 
    return financial_data[date]


def get_total(financial_data, date):

    total = 0
    for csv_date, balance in financial_data.items():
        csv_month = int(csv_date[5:])
        csv_year = int(csv_date[0:4])

        date_month = int(date.strftime('%m'))
        date_year = int(date.strftime('%Y'))

        # csv date has to be lesser or equal to input date to calculate totals for that month
        if (csv_month <= date_month and csv_year <= date_year) or (csv_month >= date_month and csv_year <= date_year-1):
            for amount in balance:
                total += amount[1]

    return total   


def update_balance(financial_data, date, donor1, amount1, donor2, amount2):

    date = date.strftime('%Y-%m')

    if date in financial_data:
        count = 0
        for donor in financial_data[date]:
            if donor[0] == donor1 and donor[1] == amount1:
                financial_data[date][count] = [donor2, amount2]
            count += 1
    else:
        financial_data[date].append([donor2, amount2])

    return financial_data[date]


'''
input will be either - 'add', 'get', 'total', 'update'
parameters will be a list of correct size. E.g for add itll be [datetime, donor, amount]
'''
def main(input_func, parameters):

    path = 'financials.csv'
    financial_data = read_csv(financial_data=dict(), path=path)
    # financial_data = dict()

    if input_func == 'add':

        date, donor, amount = parameters
        add_balance(financial_data, date, donor, amount)
        write_csv(financial_data, path)

    elif input_func == 'get':

        date = parameters[0]
        return get_balanceSheet(financial_data, date)
    
    elif input_func == 'total':

        date = parameters[0]
        return get_total(financial_data, date)
    
    elif input_func == 'update':

        date, donor1, amount1, donor2, amount2 = parameters
        update_balance(financial_data, date, donor1, amount1, donor2, amount2)
        write_csv(financial_data, path)


    return


if __name__ == "__main__":

    import call_financials