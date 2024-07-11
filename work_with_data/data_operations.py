import csv
import json
import pandas as pd
from collections import Counter, defaultdict
import dateutil.parser

##############################################
###### Example 1 - Stock prices ##############
##############################################

def try_or_none(f):
    """wraps f to return None if f raises an exception
    assumes f takes only one input"""
    def f_or_none(x):
        try: return f(x)
        except: return None
    return f_or_none
def try_parse_field(field_name, value, parser_dict):
    """try to parse value using the appropriate function from parser_dict"""
    parser = parser_dict.get(field_name) # None if no such entry
    if parser is not None:
        return try_or_none(parser)(value)
    else:
        return value
def parse_dict(input_dict, parser_dict):
    return { field_name: try_parse_field(field_name, value, parser_dict) for field_name, value in input_dict.items()}

def group_by(grouper, rows, value_transform=None):
    '''key is output of grouper, value is list of rows'''
    grouped = defaultdict(list)
    for row in rows:
        grouped[grouper(row)].append(row)
    if value_transform is None:
        return grouped
    else:
        return { key : value_transform(rows)
                 for key, rows in grouped.items() }
def picker(field_name):
    """returns a function that picks a field out of a dict"""
    return lambda row: row[field_name]
def pluck(field_name, rows):
    """turn a list of dicts into the list of field_name values"""
    return map(picker(field_name), rows)
def day_over_day_changes(grouped_rows):
    """sort the rows by date and zip with an offset to get pairs of consecutive days"""
    ordered = sorted(grouped_rows, key=picker("date"))
    return [{   "symbol"    : today["symbol"],
                "date"      : today["date"],
                "change"    : (today["closing_price"] / yesterday["closing_price"] - 1)
    } for yesterday, today in zip(ordered, ordered[1:])]


with open('txt_files\\colon_delimited_prices.txt', 'r', encoding='utf8',newline='') as f:
    reader = csv.DictReader(f, delimiter=':')
    data = [parse_dict(row, {'date': dateutil.parser.parse, 'closing_price':float}) for row in reader]
# Find max price for AAPL actions
max_aapl_price = max(row['closing_price'] for row in data if row['symbol'] == 'AAPL')
# Group rows by symbol
by_symbol = defaultdict(list)
for row in data:
    by_symbol[row["symbol"]].append(row)   
# Find max price for each of symbol
max_price_by_symbol = { symbol: max(row["closing_price"]
    for row in grouped_rows)
    for symbol, grouped_rows in by_symbol.items()
}
# Find day over day changes, key is symbol, value is list of "change" dicts
changes_by_symbol = group_by(picker("symbol"), data, day_over_day_changes)
all_changes = [change for changes in changes_by_symbol.values() for change in changes]
print("max_change", max(all_changes, key=picker("change")))
print("min_change", min(all_changes, key=picker("change")))


