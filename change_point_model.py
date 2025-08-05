import os

# Make sure 'outputs' folder exists
os.makedirs("outputs", exist_ok=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Load your data
df = pd.read_csv("data/brent_oil_prices.csv", parse_dates=['Date'])
df = df.sort_values('Date')
df.set_index('Date', inplace=True)

# Use log returns for stability
df['log_price'] = np.log(df['Price'])
data = df['log_price'].values

# Bayesian Change Point model
with pm.Model() as model:
    # Prior for change point position
    tau = pm.DiscreteUniform("tau", lower=0, upper=len(data) - 1)

    # Priors for means before and after tau
    mu1 = pm.Normal("mu1", mu=np.mean(data), sigma=1.0)
    mu2 = pm.Normal("mu2", mu=np.mean(data), sigma=1.0)

    # Shared standard deviation
    sigma = pm.HalfNormal("sigma", sigma=1.0)

    # Define the mean at each time step
    mu = pm.math.switch(tau >= np.arange(len(data)), mu1, mu2)

    # Likelihood
    obs = pm.Normal("obs", mu=mu, sigma=sigma, observed=data)

    # Sampling
    trace = pm.sample(2000, tune=1000, cores=1, return_inferencedata=True)

# Save trace plot
az.plot_trace(trace)
plt.tight_layout()
plt.savefig("outputs/change_point_trace.png")

# Extract MAP estimate of tau
tau_posterior = trace.posterior['tau'].values.flatten()
estimated_tau = int(np.median(tau_posterior))

print(f"\nEstimated change point at index: {estimated_tau}")
print(f"Date of change: {df.index[estimated_tau].date()}")

# Plot the data with the detected change point
plt.figure(figsize=(10, 5))
plt.plot(df.index, data, label='Log Price')
plt.axvline(df.index[estimated_tau], color='red', linestyle='--', label='Change Point')
plt.title('Detected Change Point in Brent Oil Prices')
plt.xlabel('Date')
plt.ylabel('Log Price')
plt.legend()
plt.tight_layout()
plt.savefig("outputs/change_point_detected.png")
plt.show()
