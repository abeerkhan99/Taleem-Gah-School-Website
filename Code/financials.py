import csv

"""

Structure = {Date (MMYY): [[Donor 1, Fees Paid], [Donor 2, Fees Paid], [Donor 3, Fees Paid] .. etc]}
Using this structure, every month we generate a report of all the donors and their fees paid.
Get the universal time first, if date exists already, allow update, else create a new month.

Store a month entry in 1 line of csv, keep it sorted. Final balances are cumulative so editing it changes all.
Sort by date first, then calculate the balance.

Functions= 
get_Donations(date)
add_donation(date, donor, amount)
get_balance(date)

"""
financial_data = dict()
