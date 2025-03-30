import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { motion } from 'framer-motion';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Gradient colors for clusters
const clusterGradients = [
  'from-green-400 to-emerald-500',
  'from-blue-400 to-indigo-500',
  'from-purple-400 to-pink-500',
  'from-amber-400 to-orange-500',
  'from-red-400 to-rose-500',
  'from-teal-400 to-cyan-500'
];

export default function Dashboard() {
  const [selectedCluster, setSelectedCluster] = useState(null);
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runClustering = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5001/api/cluster');
      
      if (response.data.status === 'success') {
        // Transform cluster data into the format we need
        const clusterData = Object.entries(response.data.cluster_sizes).map(([id, size], index) => {
          const analysis = response.data.cluster_analysis[parseInt(id)] || {};
          return {
            id: parseInt(id),
            name: analysis.label || `Cluster ${id}`,
            description: analysis.description || `${size} customers in this segment`,
            gradient: clusterGradients[index % clusterGradients.length],
            size: size,
            avgAmount: analysis.avg_transaction_amount || 0,
            topCategories: analysis.top_categories || [],
            topMerchants: analysis.top_merchants || [],
            paymentMethods: analysis.top_payment_methods || []
          };
        });
        
        setClusters(clusterData);
      } else {
        setError(response.data.message || 'Failed to run clustering analysis');
      }
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAd = (cluster) => {
    const prompt = `Generate marketing content for ${cluster.name}:
    - Average transaction amount: $${cluster.avgAmount.toFixed(2)}
    - Top categories: ${cluster.topCategories.map(([cat, _]) => cat).join(', ')}
    - Top merchants: ${cluster.topMerchants.map(([merch, _]) => merch).join(', ')}
    - Preferred payment: ${cluster.paymentMethods[0]?.[0] || 'Unknown'}`;
    alert(`Sending to ChatGPT API:\n\n${prompt}`);
    // Here you would typically make the API call to ChatGPT
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-4 bg-gradient-to-br from-gray-50 to-gray-100">
      <h1 className="text-3xl font-bold mt-8 mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-800 to-gray-600">
        Customer Segments Dashboard
      </h1>

      {/* Clustering Section */}
      <Card className="w-full max-w-4xl mb-8">
        <CardHeader>
          <CardTitle>Customer Clustering Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <Button 
            onClick={runClustering}
            disabled={loading}
            className="mb-4"
          >
            {loading ? 'Running Clustering...' : 'Run Clustering Analysis'}
          </Button>

          {error && (
            <div className="p-4 bg-red-100 text-red-700 rounded mb-4">
              Error: {error}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="w-full max-w-7xl flex">
        {/* Left side - Circle diagram */}
        <div className="w-1/2 relative flex items-center justify-center min-h-[500px]">
          {/* Central Uber circle */}
          <motion.div 
            className="w-32 h-32 rounded-full bg-gradient-to-br from-black to-gray-800 text-white flex items-center justify-center text-xl font-bold shadow-lg"
            animate={{
              boxShadow: [
                "0 4px 12px rgba(0, 0, 0, 0.1)",
                "0 8px 24px rgba(0, 0, 0, 0.2)",
                "0 4px 12px rgba(0, 0, 0, 0.1)",
              ],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          >
            Uber
          </motion.div>

          {/* Cluster circles */}
          {clusters.map((cluster, index) => {
            const angle = (index * (360 / clusters.length)) * (Math.PI / 180);
            const radius = 160;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;

            return (
              <motion.div
                key={cluster.id}
                className={`absolute w-28 h-28 rounded-full bg-gradient-to-br ${cluster.gradient} text-white border-2 border-white/20 shadow-md flex items-center justify-center text-center p-2 cursor-pointer backdrop-blur-sm`}
                style={{
                  left: 'calc(50% - 56px)',
                  top: 'calc(50% - 56px)',
                  transform: `translate(${x}px, ${y}px)`,
                  transformOrigin: 'center center'
                }}
                onClick={() => setSelectedCluster(cluster)}
                animate={{
                  boxShadow: [
                    "0 4px 12px rgba(0, 0, 0, 0.1)",
                    "0 8px 24px rgba(0, 0, 0, 0.2)",
                    "0 4px 12px rgba(0, 0, 0, 0.1)",
                  ],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut",
                  delay: index * 0.2,
                }}
              >
                <span className="text-sm font-medium">{cluster.name}</span>
              </motion.div>
            );
          })}
        </div>

        {/* Right side - Circular Card */}
        <div className="w-1/2 pl-8 flex items-center justify-center">
          {selectedCluster && (
            <motion.div
              initial={{ scale: 0, x: -100, opacity: 0 }}
              animate={{ scale: 1, x: 0, opacity: 1 }}
              transition={{
                type: "spring",
                stiffness: 260,
                damping: 20
              }}
              className="w-96 h-96 rounded-full bg-white/80 backdrop-blur-sm border-2 border-white/20 shadow-lg p-8 flex flex-col items-center justify-center text-center"
            >
              <h3 className={`text-xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r ${selectedCluster.gradient}`}>
                {selectedCluster.name}
              </h3>
              <p className="text-gray-700 mb-4 px-4">
                {selectedCluster.description}
              </p>
              <div className="text-sm text-gray-600 mb-4">
                <p>Average Transaction: ${selectedCluster.avgAmount.toFixed(2)}</p>
                <p>Top Categories: {selectedCluster.topCategories.map(([cat, _]) => cat).join(', ')}</p>
                <p>Top Merchants: {selectedCluster.topMerchants.map(([merch, _]) => merch).join(', ')}</p>
              </div>
              <Button 
                className={`bg-gradient-to-r ${selectedCluster.gradient} text-white border-none`}
                onClick={() => handleGenerateAd(selectedCluster)}
              >
                Generate Ad
              </Button>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
