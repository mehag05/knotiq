import React, { useState, useEffect } from 'react';

const ClusterProfile = ({ cluster, gradient }) => (
  <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
    <h3 className="text-2xl font-bold mb-4" style={{ background: gradient, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
      {cluster.name}
    </h3>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h4 className="text-lg font-semibold mb-2">Profile</h4>
        <p className="text-gray-600">{cluster.characteristics.join(', ')}</p>
        
        <h4 className="text-lg font-semibold mt-4 mb-2">Average Transaction</h4>
        <p className="text-gray-600">${cluster.average_transaction.toFixed(2)}</p>
        
        <h4 className="text-lg font-semibold mt-4 mb-2">Top Categories</h4>
        <ul className="space-y-1">
          {cluster.top_categories.map((cat, index) => (
            <li key={index} className="text-gray-600">
              {cat.category}: {cat.percentage.toFixed(1)}%
            </li>
          ))}
        </ul>
        
        <h4 className="text-lg font-semibold mt-4 mb-2">Top Brands</h4>
        <ul className="space-y-1">
          {cluster.top_brands.map((brand, index) => (
            <li key={index} className="text-gray-600">
              {brand.brand}: {brand.percentage.toFixed(1)}%
            </li>
          ))}
        </ul>
        <p className="text-gray-600 mt-2">
          <span className="font-semibold">Favorite Brand:</span> {cluster.favorite_brand}
        </p>
      </div>
      
      <div>
        <h4 className="text-lg font-semibold mb-2">Payment Preferences</h4>
        <ul className="space-y-1">
          {cluster.payment_methods.map((method, index) => (
            <li key={index} className="text-gray-600">
              {method.method}: {method.percentage.toFixed(1)}%
            </li>
          ))}
        </ul>
        
        <h4 className="text-lg font-semibold mt-4 mb-2">Shopping Timing</h4>
        <ul className="space-y-1">
          <li className="text-gray-600">evening: {cluster.timing.evening.toFixed(1)}%</li>
          <li className="text-gray-600">weekend: {cluster.timing.weekend.toFixed(1)}%</li>
          <li className="text-gray-600">morning: {cluster.timing.morning.toFixed(1)}%</li>
          <li className="text-gray-600">afternoon: {cluster.timing.afternoon.toFixed(1)}%</li>
        </ul>
      </div>
    </div>
  </div>
);

const CustomerPrediction = ({ prediction, gradient }) => (
  <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
    <h3 className="text-2xl font-bold mb-4" style={{ background: gradient, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
      Customer {prediction.customer_id}
    </h3>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h4 className="text-lg font-semibold mb-2">Profile</h4>
        <p className="text-gray-600">{prediction.cluster_characteristics.join(', ')}</p>
        
        <h4 className="text-lg font-semibold mt-4 mb-2">Predicted Categories</h4>
        <ul className="space-y-1">
          {prediction.predicted_categories.map((cat, index) => (
            <li key={index} className="text-gray-600">
              {cat.category}: {cat.confidence.toFixed(1)}%
            </li>
          ))}
        </ul>
        
        <h4 className="text-lg font-semibold mt-4 mb-2">Brand Preferences</h4>
        <ul className="space-y-1">
          {prediction.brand_preferences.map((brand, index) => (
            <li key={index} className="text-gray-600">
              {brand.brand}: {brand.confidence.toFixed(1)}%
            </li>
          ))}
        </ul>
        <p className="text-gray-600 mt-2">
          <span className="font-semibold">Top Brand:</span> {prediction.top_brand}
        </p>
      </div>
      
      <div>
        <h4 className="text-lg font-semibold mb-2">Likely Amount Range</h4>
        <p className="text-gray-600">
          ${prediction.likely_amount_range.min.toFixed(2)} - ${prediction.likely_amount_range.max.toFixed(2)}
        </p>
        
        <h4 className="text-lg font-semibold mt-4 mb-2">Likely Payment Methods</h4>
        <ul className="space-y-1">
          {prediction.likely_payment_methods.map((method, index) => (
            <li key={index} className="text-gray-600">
              {method.method}: {method.confidence.toFixed(1)}%
            </li>
          ))}
        </ul>
      </div>
    </div>
  </div>
);

function App() {
  const [clusters, setClusters] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  const gradientColors = [
    'linear-gradient(45deg, #FF6B6B, #4ECDC4)',
    'linear-gradient(45deg, #A8E6CF, #FFD3B6)',
    'linear-gradient(45deg, #FF8B94, #FFB5A7)',
    'linear-gradient(45deg, #95E1D3, #FCE38A)',
    'linear-gradient(45deg, #B8A7EA, #EFD5FF)'
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:5001/cluster_data');
        const data = await response.json();
        
        if (data.status === 'success') {
          // Transform cluster data to include names and gradients
          const transformedClusters = data.cluster_analysis.map((cluster, index) => ({
            ...cluster,
            name: `Cluster ${cluster.cluster_id}`,
            gradient: gradientColors[index % gradientColors.length]
          }));
          setClusters(transformedClusters);
        } else {
          setError('Failed to fetch cluster data');
        }
      } catch (err) {
        setError('Error connecting to server');
        console.error('Error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleCustomerSelect = async (customerId) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:5001/predict/${customerId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setSelectedCustomer({
          ...data.prediction,
          customer_id: customerId,
          gradient: gradientColors[data.prediction.cluster_id % gradientColors.length]
        });
      } else {
        setError('Failed to fetch prediction');
      }
    } catch (err) {
      setError('Error connecting to server');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-red-500 text-xl">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8">Customer Segmentation Analysis</h1>
        
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Customer Clusters</h2>
          <div className="grid grid-cols-1 gap-6">
            {clusters.map((cluster) => (
              <ClusterProfile key={cluster.cluster_id} cluster={cluster} gradient={cluster.gradient} />
            ))}
          </div>
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Customer Predictions</h2>
          <div className="mb-4">
            <input
              type="text"
              placeholder="Enter customer ID"
              className="px-4 py-2 border rounded-lg mr-4"
              onChange={(e) => setSelectedCustomer(e.target.value)}
            />
            <button
              onClick={() => handleCustomerSelect(selectedCustomer)}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            >
              Get Prediction
            </button>
          </div>
          {selectedCustomer && (
            <CustomerPrediction prediction={selectedCustomer} gradient={selectedCustomer.gradient} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 