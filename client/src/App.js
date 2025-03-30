import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { motion } from 'framer-motion';
import React, { useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [merchantName, setMerchantName] = useState('');
  const [merchantData, setMerchantData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchMerchant = async () => {
    if (!merchantName.trim()) {
      setError('Please enter a merchant name');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:5001/api/merchant/${encodeURIComponent(merchantName)}/top-customers`);
      
      if (response.data.status === 'success') {
        setMerchantData(response.data);
      } else {
        setError('Failed to fetch merchant data');
      }
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-4 bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Search Section */}
      <div className="w-full max-w-4xl mt-8 mb-8">
        <Card className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
          <CardContent className="p-8">
            <h1 className="text-3xl font-bold mb-6 text-center">Merchant Analytics Dashboard</h1>
            <div className="flex gap-4">
              <input
                type="text"
                value={merchantName}
                onChange={(e) => setMerchantName(e.target.value)}
                placeholder="Enter merchant name (e.g., Carvana, Amazon Prime, Costco)"
                className="flex-1 px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/40"
                onKeyPress={(e) => e.key === 'Enter' && searchMerchant()}
              />
              <Button
                onClick={searchMerchant}
                disabled={loading}
                className="bg-white text-blue-600 hover:bg-white/90"
              >
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {error && (
        <div className="w-full max-w-4xl mb-8">
          <div className="p-4 bg-red-100 text-red-700 rounded-lg">
            Error: {error}
          </div>
        </div>
      )}

      {merchantData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-4xl"
        >
          <h2 className="text-2xl font-bold mb-6 text-gray-800">{merchantData.merchant_name}</h2>

          {/* Key Metrics */}
          <div className="grid grid-cols-4 gap-4 mb-8">
            <Card className="bg-white">
              <CardContent className="p-6">
                <div className="text-2xl font-bold text-blue-600">{merchantData.demographics.total_customers}</div>
                <div className="text-sm text-gray-600">Total Customers</div>
              </CardContent>
            </Card>
            <Card className="bg-white">
              <CardContent className="p-6">
                <div className="text-2xl font-bold text-green-600">
                  ${merchantData.demographics.average_transaction_value.toFixed(2)}
                </div>
                <div className="text-sm text-gray-600">Avg Transaction</div>
              </CardContent>
            </Card>
            <Card className="bg-white">
              <CardContent className="p-6">
                <div className="text-2xl font-bold text-emerald-600">
                  {merchantData.demographics.retention_metrics.retention_rate}%
                </div>
                <div className="text-sm text-gray-600">Retention Rate</div>
              </CardContent>
            </Card>
            <Card className="bg-white">
              <CardContent className="p-6">
                <div className="text-2xl font-bold text-red-600">
                  {merchantData.demographics.retention_metrics.churn_rate}%
                </div>
                <div className="text-sm text-gray-600">Churn Rate</div>
              </CardContent>
            </Card>
          </div>

          {/* Top Customers */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Top Customers</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {merchantData.top_customers.map((customer, index) => (
                  <div key={index} className="bg-white rounded-lg p-4 border border-gray-100 shadow-sm">
                    <div className="flex justify-between items-center">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-800">Customer {customer.customer_id}</h3>
                        <p className="text-sm text-gray-600">CLV Score: ${customer.clv_score.toFixed(2)}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Frequency: {customer.purchase_frequency.toFixed(2)}/month</p>
                        <p className="text-sm text-gray-600">Avg Transaction: ${customer.avg_transaction_value.toFixed(2)}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
