import React, { useState } from 'react';
import { Button } from './ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import OpenAIUtils from '../utils/openai';

export default function CustomerProfile({ profile, merchantName }) {
  const [generatedAd, setGeneratedAd] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateAd = async () => {
    setLoading(true);
    setError(null);
    try {
      const segment = {
        name: merchantName,
        description: profile
      };
      
      const adPrompt = await OpenAIUtils.generateAdPrompt(merchantName, segment, "products");
      console.log("Generated ad prompt:", adPrompt);

      const response = await fetch('http://localhost:5001/api/text_to_image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'image/png'
        },
        body: JSON.stringify({ prompt: adPrompt })
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server response:', errorText);
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setGeneratedAd({
        prompt: adPrompt,
        imageUrl: imageUrl
      });
    } catch (error) {
      console.error('Full error details:', error);
      setError('Error generating ad: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  if (!profile) return null;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-5xl mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-12"
        >
          {/* Header Section */}
          <div className="bg-black rounded-3xl p-12 text-center mb-12">
            <h1 className="text-4xl font-bold text-white mb-4">
              Customer Insights
            </h1>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Understand your top customers and generate targeted advertisements
            </p>
          </div>

          {/* Customer Profile Section */}
          <div className="bg-white rounded-3xl p-10 shadow-lg border border-gray-100">
            <div className="flex items-start justify-between gap-12">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-2 h-2 bg-black rounded-full"></div>
                  <h2 className="text-2xl font-semibold text-black">Customer Profile</h2>
                </div>
                <p className="text-gray-600 text-lg leading-relaxed">
                  {profile}
                </p>
              </div>
              <Button 
                className="bg-black hover:bg-gray-900 text-white px-8 py-3 rounded-xl shadow-md hover:shadow-lg transition-all duration-200 flex items-center gap-3 font-medium text-lg"
                onClick={handleGenerateAd}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                    />
                    Generating...
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                    </svg>
                    Generate Ad
                  </>
                )}
              </Button>
            </div>
          </div>

          {/* Error Message */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="bg-gray-50 border border-gray-200 rounded-2xl p-8"
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-gray-100 rounded-full">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-900" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-xl font-medium text-gray-900">Error</p>
                    <p className="text-gray-700 mt-2 text-lg">{error}</p>
                    <p className="mt-3 text-sm text-gray-500 bg-gray-100/50 p-4 rounded-xl">Make sure the text-to-image server is running with: modal serve text_to_image.py</p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Generated Ad Section */}
          <AnimatePresence>
            {generatedAd && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.3 }}
              >
                <div className="bg-white rounded-3xl p-10 shadow-lg border border-gray-100">
                  <div className="flex items-center gap-3 mb-8">
                    <div className="w-2 h-2 bg-black rounded-full"></div>
                    <h2 className="text-2xl font-semibold text-black">Generated Ad</h2>
                  </div>
                  <div className="relative aspect-video w-full overflow-hidden rounded-2xl shadow-xl">
                    <motion.img 
                      initial={{ opacity: 0, scale: 1.1 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.5 }}
                      src={generatedAd.imageUrl} 
                      alt="Generated advertisement"
                      className="object-cover w-full h-full"
                    />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
} 