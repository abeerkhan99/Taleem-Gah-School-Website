import csv
import datetime
"""

Structure = 

.csv
{Date (MMYY): [[Donor 1, Amount], [Donor 2, Amount], [Donor 3, Amount] .. etc]}
Identifier + Date:
-Balance Sheet
-Total

Identifier + Date: .. etc

Using this structure, every month we generate a report of all the donors and their fees paid.
Get the universal time first, if date exists already, allow update, else create a new month.

Store a month entry in 1 line of csv, keep it sorted. Final balances are cumulative so editing it changes all.
Sort by date first, then calculate the balance.

Functions= 
get_balanceSheet(date)
add_balance(date, donor, amount)
get_total(date)

"""

financial_data = dict()

def read_csv():
    with open('financials.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            financial_data[row[0]] = row[1:]

def write_csv(financial_data):
    with open('financials.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in financial_data.items():
            writer.writerow([key, value])

def get_balanceSheet(date):

    if date in financial_data:
        return financial_data[date]
    else:
        return []


def add_balance(date, donor, amount):

    if date in financial_data:
        financial_data[date].append([donor, amount])
    else:
        financial_data[date] = [[donor, amount]]

    financial_data[date].sort(key=lambda x: x[1], reverse=True)

    return financial_data[date]


def get_total(date):
    total = 0
    for donor in get_balanceSheet(date):
        total += donor[1]
    return total   


def main():

    get_balanceSheet(datetime.datetime(2020, 5, 17))
    add_balance(datetime.datetime(2020, 5, 17), "Donor 1", 100)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 2", 200)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 3", 300)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 4", 400)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 5", 500)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 6", 600)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 7", 700)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 8", 800)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 9", 900)
    add_balance(datetime.datetime(2020, 5, 17), "Donor 10", 1000)

    print(get_total(datetime.datetime(2020, 5, 17)))


if __name__ == "__main__":

    main()