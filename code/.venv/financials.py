import csv
import datetime
import pandas as pd
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


def get_total(financial_data, start_date, end_date = None):

    total = 0
    total_balance_sheet = []

    startdate_month = int(start_date.strftime('%m'))
    startdate_year = int(start_date.strftime('%Y'))

    if end_date != None:
        enddate_month = int(end_date.strftime('%m'))
        enddate_year = int(end_date.strftime('%Y'))

    for csv_date, balance in financial_data.items():
        csv_month = int(csv_date[5:])
        csv_year = int(csv_date[0:4])

        if end_date != None:
    
            # for different start and end year
            if startdate_year < enddate_year:
                # csv_month must be greater or equal to csv_month and csv_year must be equal to start year
                # csv_month must be less than or equal to csv_month and csv_year must be equal to end_year
                if ((csv_month >= startdate_month and csv_year == startdate_year) or (csv_month <= enddate_month and csv_year == enddate_year)):
                    for amount in balance:
                        total_balance_sheet.append([csv_month, csv_year, amount])
                        total += amount[1]

            elif startdate_year > enddate_year:
                if ((csv_month >= enddate_month and csv_year == enddate_year) or (csv_month <= startdate_month and csv_year == startdate_year)):
                    for amount in balance:
                        total_balance_sheet.append([csv_month, csv_year, amount])
                        total += amount[1]

            # for same year
            # csv_month must be greater than start date month and less than or equal to end date month
            # and csv_year must equal startdate year and end date year
            elif ((csv_month >= startdate_month) and (csv_month <= enddate_month)) and ((csv_year == startdate_year) and (csv_year == enddate_year)):
                for amount in balance:
                    total_balance_sheet.append([csv_month, csv_year, amount])
                    total += amount[1]

        elif end_date == None:
            # to get all data
            if (csv_month <= startdate_month and csv_year <= startdate_year):
                for amount in balance:
                    total_balance_sheet.append([csv_month, csv_year, amount])
                    total += amount[1]

            else:
                total = "Error!"

    if startdate_year > enddate_year:

        # total_balance_sheet.sort(reverse = True)
        total_balance_sheet.sort(key=lambda x:(x[0], x[1], x[2][1]), reverse=True)
    else:
        # total_balance_sheet.sort()
        total_balance_sheet.sort(key=lambda x:(x[0], x[1], x[2][1]))


    total_balance_sheet.append(total)
    return total_balance_sheet  


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

def get_info(financial_data, date):
    info = []
    year = []

    for csv_date in financial_data.items():
        csv_info = csv_date[0]
        y_m = csv_info.split("-")
        info.append(y_m)
        if y_m[0] not in year:
            year.append(y_m[0])
    year.sort()
    return year

def delete_balance(financial_data, date):
    date = date.strftime('%Y-%m')
    
    if date in financial_data:
        del financial_data[date]


'''
input will be either - 'add', 'get', 'total', 'update'
parameters will be a list of correct size. E.g for add itll be [datetime, donor, amount]
'''
def main(input_func, parameters, end_p = None):

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

        start_date = parameters[0]
        if end_p != None:
            end_date =  end_p[0]
            return get_total(financial_data, start_date, end_date)
        else:
            return get_total(financial_data, start_date)
    
    elif input_func == 'update':

        date, donor1, amount1, donor2, amount2 = parameters
        update_balance(financial_data, date, donor1, amount1, donor2, amount2)
        write_csv(financial_data, path)

    elif input_func == "info":
        return get_info(financial_data, parameters)

    elif input_func == "delete":
        # print(financial_data)

        date = parameters[0]
        delete_balance(financial_data, date)
        write_csv(financial_data, path)

    return
    
# f = open('financials.csv', 'w+')
# f.close()
# main('add', [datetime.datetime.today(), 'Donor 1', 1000])
# main('add', [datetime.datetime.today(), 'Donor 2', 100])
# # main('add', [datetime.datetime(2001, 1, 12), 'Donor 3', 200])
# # main('add', [datetime.datetime(2001, 1, 12), 'Donor 5', 300])
# main('add', [datetime.datetime.today(), 'Donor 7', 10000])
# main('add', [datetime.datetime(2022, 9, 12), 'Expense 1', -300])
# main('add', [datetime.datetime(2021, 8, 12), 'Donor 5', 300])
# main('add', [datetime.datetime(2021, 7, 12), 'Donor 5', 300])
# main('add', [datetime.datetime(2021, 6, 12), 'Donor 5', 300])
# main('add', [datetime.datetime(2022, 8, 12), 'Expense 1', -500])


# main('update', [datetime.datetime.today(), 'Donor 2', 100, 'Donor 11', 1])

# #this gets all the info in the file
# # print(main('get', [datetime.datetime.today()]))

# #this calculates all the info in the file
# # print(main('total', [datetime.datetime.today()]))
# # print(main('total',[datetime.datetime(2022, 9, 12)], [datetime.datetime(2021, 6, 12)]))
# print(main('total',[datetime.datetime(2021, 6, 12)], [datetime.datetime(2022, 9, 12)]))

# # print(main("info", [datetime.datetime.today()]))
