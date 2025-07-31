import pandas as pd
import numpy as np

# Generate date range
dates = pd.date_range(start='2019-01-01', end='2021-12-31', freq='D')
n = len(dates)

# Create price segments with different means for 3 change points
# 2019: ~60, 2020: ~70, 2021: ~50
prices = np.empty(n)

for i, date in enumerate(dates):
    if date < pd.Timestamp('2020-01-01'):
        prices[i] = 60 + np.random.normal(0, 0.5)  # around 60 with noise
    elif date < pd.Timestamp('2021-01-01'):
        prices[i] = 70 + np.random.normal(0, 1.0)  # around 70 with more noise
    else:
        prices[i] = 50 + np.random.normal(0, 0.7)  # around 50 with some noise

# Create DataFrame and save
df_prices = pd.DataFrame({'Date': dates, 'Price': prices})
df_prices.to_csv('brent_oil_prices.csv', index=False)

# Create events DataFrame
events = {
    'Event Name': ['Event A', 'Event B', 'Event C', 'Event D', 'Event E'],
    'Date': ['2019-06-15', '2020-02-15', '2020-12-01', '2021-03-01', '2021-11-15'],
    'Description': [
        'Trade tensions escalate',
        'Global pandemic impacts demand',
        'OPEC announces production cuts',
        'Geopolitical conflict disrupts supply',
        'Market recovers on vaccine news'
    ]
}

df_events = pd.DataFrame(events)
df_events['Date'] = pd.to_datetime(df_events['Date'])
df_events.to_csv('key_events.csv', index=False)

print("Files 'brent_oil_prices.csv' and 'key_events.csv' created successfully!")
