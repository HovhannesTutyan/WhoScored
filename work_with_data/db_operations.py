import yfinance as yf
import sqlite3

data = []
tickers = ['TSLA', 'FB', 'ORCL', 'AMZN']
for ticker in tickers:
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period='5d').reset_index()
    # Take only date and close data
    records = hist[['Date', 'Close']].to_records(index=False)
    # Convert data to list, to be able to save it in db
    records = list(records)
    # Format data by taking only 10 symbols from the date, and round close price
    records = [(ticker, str(elem[0])[:10], round(elem[1], 2)) for elem in records]
    data.extend(records)  # Use extend instead of + for efficiency

print(data)

# Transfer data to SQLite db
conn = sqlite3.connect("ticker.db")
with conn:
    cur = conn.cursor()
    # Create the stocks table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            date TEXT,
            price REAL
        )
    """)
    # Insert data into the stocks table
    query_add_stocks = "INSERT INTO stocks (ticker, date, price) VALUES (?, ?, ?)"
    cur.executemany(query_add_stocks, data)
    conn.commit()

print("Data has been successfully inserted into the database.")