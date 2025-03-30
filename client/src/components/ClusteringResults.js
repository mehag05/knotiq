import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ClusteringResults = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [results, setResults] = useState(null);
    const [visualizations, setVisualizations] = useState(null);

    const runClustering = async () => {
        setLoading(true);
        setError(null);
        try {
            // Run clustering
            const response = await axios.post('http://localhost:5000/api/cluster');
            setResults(response.data);

            // Get visualizations
            const vizResponse = await axios.get('http://localhost:5000/api/visualizations');
            setVisualizations(vizResponse.data.visualizations);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold mb-4">Customer Clustering Results</h2>
            
            <button
                onClick={runClustering}
                disabled={loading}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
            >
                {loading ? 'Running Clustering...' : 'Run Clustering'}
            </button>

            {error && (
                <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
                    Error: {error}
                </div>
            )}

            {results && (
                <div className="mt-6">
                    <h3 className="text-xl font-semibold mb-2">Clustering Metrics</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="p-4 bg-white rounded shadow">
                            <h4 className="font-medium">Silhouette Score</h4>
                            <p className="text-2xl">{results.metrics.silhouette.toFixed(3)}</p>
                        </div>
                        <div className="p-4 bg-white rounded shadow">
                            <h4 className="font-medium">Calinski-Harabasz Score</h4>
                            <p className="text-2xl">{results.metrics.calinski_harabasz.toFixed(3)}</p>
                        </div>
                        <div className="p-4 bg-white rounded shadow">
                            <h4 className="font-medium">Davies-Bouldin Score</h4>
                            <p className="text-2xl">{results.metrics.davies_bouldin.toFixed(3)}</p>
                        </div>
                    </div>

                    <h3 className="text-xl font-semibold mt-6 mb-2">Visualizations</h3>
                    {visualizations && (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="p-4 bg-white rounded shadow">
                                <h4 className="font-medium mb-2">Cluster PCA</h4>
                                <img
                                    src={visualizations.clusters_pca}
                                    alt="Cluster PCA"
                                    className="w-full h-auto"
                                />
                            </div>
                            <div className="p-4 bg-white rounded shadow">
                                <h4 className="font-medium mb-2">Feature Correlation</h4>
                                <img
                                    src={visualizations.feature_correlation}
                                    alt="Feature Correlation"
                                    className="w-full h-auto"
                                />
                            </div>
                            <div className="p-4 bg-white rounded shadow">
                                <h4 className="font-medium mb-2">Elbow Analysis</h4>
                                <img
                                    src={visualizations.elbow_analysis}
                                    alt="Elbow Analysis"
                                    className="w-full h-auto"
                                />
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ClusteringResults; 