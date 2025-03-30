import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { motion } from 'framer-motion';
import React, { useState } from 'react';
import OpenAIUtils from './utils/openaiutils.js';


const customerSegments = [
  {
    id: 1,
    name: 'Health-Conscious Millennials',
    description: 'Urban professionals aged 25–35 who frequently purchase organic food, supplements, and fitness gear.',
    gradient: 'from-green-400 to-emerald-500',
  },
  {
    id: 2,
    name: 'Tech-Savvy Professionals',
    description: 'Customers with recurring purchases from Amazon, Best Buy, and Netflix.',
    gradient: 'from-blue-400 to-indigo-500',
  },
  {
    id: 3,
    name: 'Pet-First Shoppers',
    description: 'Shoppers with regular purchases from PetSmart and Costco.',
    gradient: 'from-purple-400 to-pink-500',
  },
  {
    id: 4,
    name: 'Luxury Shoppers',
    description: 'High-income individuals who frequently shop at premium retailers and luxury brands.',
    gradient: 'from-amber-400 to-orange-500',
  },
  {
    id: 5,
    name: 'Family-Focused',
    description: 'Parents and guardians who prioritize family-oriented products and services.',
    gradient: 'from-red-400 to-rose-500',
  },
  {
    id: 6,
    name: 'Budget Conscious',
    description: 'Value-seeking customers who prioritize deals and discounts.',
    gradient: 'from-teal-400 to-cyan-500',
  }
];


export default function Dashboard() {
  const [selectedSegment, setSelectedSegment] = useState(null);
  const [generatedImageUrl, setGeneratedImageUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateAd = async (segment, merchantName, productName) => {
    try {
      // Use await to resolve the promise
      const promptContent = await OpenAIUtils.generateAdPrompt(merchantName, segment, productName);
      console.log(promptContent); 

      setIsLoading(true);
      setError(null);
      setGeneratedImageUrl(null);
  
      try {
        const imageUrl = await generateImage(promptContent);
        console.log('Image generated:', imageUrl);
        setGeneratedImageUrl(imageUrl);
      } catch (error) {
        console.error('Error:', error);
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    } catch (error) {
      console.error("Error getting prompt:", error);
    }
  };

  async function generateImage(prompt) {
    try {
      const MODAL_URL = "https://slee37--example-text-to-image-ui.modal.run";
      
      const response = await fetch(`${MODAL_URL}/api/text_to_image`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Image generation failed');
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);

      return imageUrl;
    } catch (error) {
      console.error('Failed to generate image:', error);
      throw error;
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center p-4 bg-gradient-to-br from-gray-50 to-gray-100">
      <h1 className="text-3xl font-bold mt-8 mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-800 to-gray-600">
        Customer Segments Dashboard
      </h1>
      <div className="w-full max-w-7xl flex flex-col md:flex-row">
        {/* Left side - Circle diagram */}
        <div className="w-full md:w-1/2 relative flex items-center justify-center min-h-[500px]">
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

          {/* Segment circles */}
          {customerSegments.map((segment, index) => {
            const angle = (index * (360 / customerSegments.length)) * (Math.PI / 180);
            const radius = 160;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;

            return (
              <motion.div
                key={segment.id}
                className={`absolute w-28 h-28 rounded-full bg-gradient-to-br ${segment.gradient} text-white border-2 border-white/20 shadow-md flex items-center justify-center text-center p-2 cursor-pointer backdrop-blur-sm`}
                style={{
                  left: 'calc(50% - 56px)',
                  top: 'calc(50% - 56px)',
                  transform: `translate(${x}px, ${y}px)`,
                  transformOrigin: 'center center'
                }}
                onClick={() => setSelectedSegment(segment)}
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
                <span className="text-sm font-medium">{segment.name}</span>
              </motion.div>
            );
          })}
        </div>

        {/* Right side - Circular Card and Generated Image */}
        <div className="w-full md:w-1/2 pl-0 md:pl-8 flex flex-col items-center justify-center">
          {selectedSegment && (
            <motion.div
              initial={{ scale: 0, x: -100, opacity: 0 }}
              animate={{ scale: 1, x: 0, opacity: 1 }}
              transition={{
                type: "spring",
                stiffness: 260,
                damping: 20
              }}
              className="w-96 h-96 rounded-full bg-white/80 backdrop-blur-sm border-2 border-white/20 shadow-lg p-8 flex flex-col items-center justify-center text-center mb-6"
            >
              <h3 className={`text-xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r ${selectedSegment.gradient}`}>
                {selectedSegment.name}
              </h3>
              <p className="text-gray-700 mb-6 px-4">
                {selectedSegment.description}
              </p>
              <Button 
                className={`bg-gradient-to-r ${selectedSegment.gradient} text-white border-none`}
                onClick={() => handleGenerateAd(selectedSegment, "Uber", "Uber Eats")}
                disabled={isLoading}
              >
                {isLoading ? 'Generating...' : 'Generate Ad'}
              </Button>
            </motion.div>
          )}

          {/* Loading indicator */}
          {isLoading && (
            <div className="mt-6 text-center">
              <div className="w-8 h-8 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin mx-auto mb-2"></div>
              <p className="text-gray-600">Generating image...</p>
            </div>
          )}

          {/* Error message */}
          {error && (
            <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-lg max-w-md">
              <p className="font-bold">Error:</p>
              <p>{error}</p>
            </div>
          )}

          {/* Generated image */}
          {generatedImageUrl && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mt-6 max-w-md w-full"
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-center">Generated Ad</CardTitle>
                </CardHeader>
                <CardContent>
                  <img 
                    src={generatedImageUrl} 
                    alt="Generated Ad" 
                    className="w-full h-auto rounded-lg shadow-md"
                  />
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}