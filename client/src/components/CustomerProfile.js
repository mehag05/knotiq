import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { motion } from 'framer-motion';
import OpenAIUtils from '../utils/openai';

export default function CustomerProfile({ profile, merchantName }) {
  const [generatedAd, setGeneratedAd] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateAd = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/text_to_image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'image/png'
        },
        body: JSON.stringify({ prompt: profile })
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server response:', errorText);
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setGeneratedAd({
        prompt: profile,
        imageUrl: imageUrl
      });
    } catch (error) {
      console.error('Full error details:', error);
      setError('Error generating ad: ' + error.message);
    }
  };

  if (!profile) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* Customer Profile Section */}
      <Card className="bg-white">
        <CardHeader>
          <CardTitle className="text-xl font-bold text-gray-800">Customer Profile</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-gray-700 text-lg">
                {profile}
              </p>
            </div>
            <Button 
              className="ml-4 bg-blue-600 hover:bg-blue-700 text-white"
              onClick={handleGenerateAd}
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate Ad'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Generated Ad Section */}
      {error && (
        <div className="p-4 bg-red-100 text-red-700 rounded-lg">
          <p className="font-semibold">Error:</p>
          <p>{error}</p>
          <p className="mt-2 text-sm">Make sure the text-to-image server is running with: modal serve text_to_image.py</p>
        </div>
      )}

      {generatedAd && (
        <Card className="bg-white">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-gray-800">Generated Ad</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="aspect-video relative rounded-lg overflow-hidden">
                <img 
                  src={generatedAd.imageUrl} 
                  alt="Generated advertisement"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Ad Prompt</h3>
                <p className="text-gray-600 whitespace-pre-wrap">{generatedAd.prompt}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </motion.div>
  );
} 