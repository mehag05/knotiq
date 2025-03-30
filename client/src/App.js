import React, { useState } from 'react';
import { motion } from 'framer-motion';
import CustomerProfile from './components/CustomerProfile';
import knotLogo from './assets/knot_logo.png';

function App() {
  const [merchantData, setMerchantData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchMerchant = async (merchantName) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:5001/api/merchant/${encodeURIComponent(merchantName)}/top-customers`);
      if (!response.ok) {
        throw new Error('Failed to fetch merchant data');
      }
      const data = await response.json();
      setMerchantData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Header */}
      <div className="bg-black text-white py-8">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-start">
            <a href="https://www.knotapi.com" target="_blank" rel="noopener noreferrer">
              <img src={knotLogo} alt="Knot Logo" className="h-12 w-auto -mt-2" />
            </a>
          </div>
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-2">Market Analytics Dashboard</h1>
            <p className="text-gray-300">Analyze customer behavior and generate targeted advertisements</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Search Section */}
        <div className="max-w-2xl mx-auto mb-12">
          <div className="bg-white rounded-3xl p-8 shadow-lg border border-gray-100">
            <h2 className="text-2xl font-semibold text-black mb-6">Search Merchant</h2>
            <div className="flex gap-4">
              <input
                type="text"
                placeholder="Enter merchant name..."
                className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-black"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    searchMerchant(e.target.value);
                  }
                }}
              />
              <button
                onClick={() => searchMerchant(document.querySelector('input').value)}
                className="bg-black hover:bg-gray-900 text-white px-6 py-3 rounded-xl shadow-md hover:shadow-lg transition-all duration-200 flex items-center gap-2 font-medium"
              >
                {loading ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                    />
                    Searching...
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                    </svg>
                    Search
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-gray-50 border border-gray-200 rounded-2xl p-8 mb-12">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-gray-100 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-900" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <p className="text-xl font-medium text-gray-900">Error</p>
                <p className="text-gray-700 mt-2 text-lg">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {merchantData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-12"
          >
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                { 
                  label: 'Total Customers', 
                  value: merchantData.demographics.total_customers || 0 
                },
                { 
                  label: 'Average Transaction', 
                  value: `$${(merchantData.demographics.average_transaction_value || 0).toFixed(2)}` 
                },
                { 
                  label: 'Retention Rate', 
                  value: `${(merchantData.demographics.retention_metrics.retention_rate || 0).toFixed(1)}%`,
                  color: 'text-green-600'
                },
                { 
                  label: 'Churn Rate', 
                  value: `${(merchantData.demographics.retention_metrics.churn_rate || 0).toFixed(1)}%`,
                  color: 'text-red-600'
                }
              ].map((metric, index) => (
                <div key={index} className="bg-white rounded-3xl p-6 shadow-lg border border-gray-100">
                  <h3 className="text-gray-600 text-sm font-medium mb-2">{metric.label}</h3>
                  <p className={`text-2xl font-bold ${metric.color || 'text-black'}`}>{metric.value}</p>
                </div>
              ))}
            </div>

            {/* Customer Profile */}
            <CustomerProfile 
              profile={merchantData.profile}
              merchantName={merchantData.merchant_name}
            />
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;
