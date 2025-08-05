from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/oil-prices', methods=['GET'])
def get_oil_prices():
    df = pd.read_csv('data/brent_oil_prices.csv')
    return df.to_json(orient='records')

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    with open('data/change_points.json', 'r') as f:
        change_points = json.load(f)
    return jsonify(change_points)

@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    df = pd.read_csv('data/indicators.csv')
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
