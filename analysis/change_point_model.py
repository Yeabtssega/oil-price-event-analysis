import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymc3 as pm
import arviz as az
import os

# === Load Data ===
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

brent_df = pd.read_csv(os.path.join(DATA_PATH, 'brent_oil_prices.csv'), parse_dates=['Date'])
events_df = pd.read_csv(os.path.join(DATA_PATH, 'key_events.csv'), parse_dates=['Date'])

# === Quick EDA ===
print("Brent Oil Data Overview:")
print(brent_df.info())
print(brent_df.describe())

plt.figure(figsize=(12, 6))
plt.plot(brent_df['Date'], brent_df['Price'], label='Brent Price')
plt.title("Brent Oil Prices Over Time")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(DATA_PATH, 'brent_price_trend.png'))
plt.close()

# === Bayesian Change Point Model ===
prices = brent_df['Price'].values
n = len(prices)
idx = np.arange(n)

with pm.Model() as model:
    cp = pm.DiscreteUniform('cp', lower=0, upper=n-1)

    mu1 = pm.Normal('mu1', mu=np.mean(prices), sigma=10)
    mu2 = pm.Normal('mu2', mu=np.mean(prices), sigma=10)

    sigma = pm.HalfNormal('sigma', sigma=10)

    mu = pm.math.switch(idx < cp, mu1, mu2)

    obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=prices)

    trace = pm.sample(2000, tune=1000, cores=2, target_accept=0.95, progressbar=True)

# === Analyze Result ===
cp_est = int(trace['cp'].mean())
change_date = brent_df['Date'].iloc[cp_est]

print(f"\nEstimated Change Point Index: {cp_est}")
print(f"Estimated Change Point Date: {change_date.date()}")

# === Plot Results ===
plt.figure(figsize=(14, 6))
plt.plot(brent_df['Date'], prices, label='Brent Price')
plt.axvline(change_date, color='red', linestyle='--', label=f'Change Point ~ {change_date.date()}')
plt.title("Bayesian Change Point Detection on Brent Prices")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(DATA_PATH, 'change_point_detected.png'))
plt.close()

# === Cross-check with Events ===
window = pd.Timedelta(days=30)
event_window = events_df[
    (events_df['Date'] >= change_date - window) &
    (events_df['Date'] <= change_date + window)
]

if not event_window.empty:
    print("\nEvents within ±30 days of detected change point:")
    print(event_window[['Date', 'Event Name', 'Description']])
else:
    print("\nNo events found within ±30 days of detected change point.")

# === Optional: Save summary ===
summary_path = os.path.join(DATA_PATH, 'change_point_summary.txt')
with open(summary_path, 'w') as f:
    f.write(f"Estimated Change Point: {change_date.date()}\n")
    if not event_window.empty:
        f.write("Nearby Events:\n")
        f.write(event_window.to_string(index=False))
    else:
        f.write("No events within ±30 days of detected change point.\n")

print("\nAnalysis complete. Plots and summary saved in /data folder.")
