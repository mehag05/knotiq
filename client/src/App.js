import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { motion } from 'framer-motion';
import React, { useState } from 'react';

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

const generatePrompt = (segment) => {
  return `As a professional designer and marketer, generate an engaging Instagram post for Uber targeting ${segment.name}. 

Context: ${segment.description}

Please provide:
1. A compelling visual description (image/graphic concept)
2. Attention-grabbing headline (max 70 characters)
3. Engaging caption (include emojis, max 200 characters)
4. 3-5 relevant hashtags
5. Call-to-action

The post should resonate with this specific audience segment while maintaining Uber's brand voice: professional yet approachable, innovative, and customer-focused.`;
};

export default function Dashboard() {
  const [selectedSegment, setSelectedSegment] = useState(null);

  const handleGenerateAd = (segment) => {
    const prompt = generatePrompt(segment);
    alert(`Sending to ChatGPT API:\n\n${prompt}`);
    // Here you would typically make the API call to ChatGPT
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-4 bg-gradient-to-br from-gray-50 to-gray-100">
      <h1 className="text-3xl font-bold mt-8 mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-800 to-gray-600">
        Customer Segments Dashboard
      </h1>
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

        {/* Right side - Circular Card */}
        <div className="w-1/2 pl-8 flex items-center justify-center">
          {selectedSegment && (
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
              <h3 className={`text-xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r ${selectedSegment.gradient}`}>
                {selectedSegment.name}
              </h3>
              <p className="text-gray-700 mb-6 px-4">
                {selectedSegment.description}
              </p>
              <Button 
                className={`bg-gradient-to-r ${selectedSegment.gradient} text-white border-none`}
                onClick={() => handleGenerateAd(selectedSegment)}
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
