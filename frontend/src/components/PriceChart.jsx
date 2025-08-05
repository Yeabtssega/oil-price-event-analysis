import events from './events';
import { ReferenceLine } from 'recharts';
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import axios from 'axios';

const PriceChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/oil-prices').then(res => {
      const formatted = res.data.map(d => ({
        date: d.Date,
        price: parseFloat(d.Price),
      }));
      setData(formatted);
    });
  }, []);

  return (
    <div>
      <h3>Brent Oil Prices Over Time</h3>
      <LineChart width={800} height={400} data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <CartesianGrid strokeDasharray="3 3" />
        <Line type="monotone" dataKey="price" stroke="#8884d8" dot={false} />
      </LineChart>
    </div>
  );
};

export default PriceChart;
