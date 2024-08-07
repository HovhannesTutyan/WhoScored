import os
import csv
import json
import pandas as pd

                ###########################################
                # Working with text files, write and read #
                ###########################################
                
# ============== Data with tabulation ===============
# with open('dataScience\\tab_delimited_prices.txt', mode='r') as f:
#     reader = csv.reader(f, delimiter='\t')
#     for row in reader:
#         date=row[0]
#         symbol=row[1]
#         closing_price=float(row[2])
#         print(date, symbol, closing_price)

# ============== Data with comma separation ===============
# with open('dataScience\\files\\colon_delimited_prices.txt', 'r', encoding='utf8',newline='') as f:
#         reader = csv.DictReader(f, delimiter=':')
#         # reader = csv.DictReader(codecs.iterdecode(f, 'utf-8'), delimiter=':')
#         for row in reader:
#             date = row["date"]
#             symbol = row["symbol"]
#             closing_price = float(row["closing_price"])
#             print(date, symbol, closing_price)

# ============== Write to a txt file ===============
# today_prices = [
#     {'date':'19/02/2024', 'symbol':'AAPL',  'value' : 90.91}, 
#     {'date':'20/02/2024', 'symbol':'MSFT',  'value' : 41.68}, 
#     {'date':'21/02/2024', 'symbol':'FB',    'value' : 64.5}
# ]
# output = '\n'.join([f"{item['date']}, {item['symbol']}, {item['value']}" for item in today_prices])
# with open('dataScience\\files\\comma_delimited_prices.txt', 'w') as file:
#     file.write(output)

# l =  {"cars":
#   [{"Year": "1997", "Make": "Ford", "Model": "E350", "Price": "3200.00"},
#    {"Year": "1999", "Make": "Chevy", "Model": "Venture", "Price": "4800.00"},
#    {"Year": "1996", "Make": "Jeep", "Model": "Grand Cherokee", "Price": "4900.00"}
# ]}

# import json
# jsonString = json.dumps(l)
# jsonFile = open("cars.json", "w")
# jsonFile.write(jsonString)
# jsonFile.close() 

# jsonFile = open("cars.json", "r")
# pobj = json.load(jsonFile)

# for car in pobj["cars"]:  
#   for item in car.items():
#     print(item[0],':', item[1])
#   print('\n')

