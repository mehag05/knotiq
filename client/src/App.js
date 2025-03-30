import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { motion, AnimatePresence } from 'framer-motion';
import React, { useState } from 'react';

const moods = [
  { text: "Lucky", gradient: "from-green-400 to-emerald-500", emoji: "🍀" },
  { text: "Creative", gradient: "from-blue-400 to-indigo-500", emoji: "🎨" },
  { text: "Energetic", gradient: "from-purple-400 to-pink-500", emoji: "⚡" },
  { text: "Inspired", gradient: "from-amber-400 to-orange-500", emoji: "💡" },
  { text: "Bold", gradient: "from-red-400 to-rose-500", emoji: "🦁" },
  { text: "Innovative", gradient: "from-teal-400 to-cyan-500", emoji: "🚀" }
];

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
  const [currentMood, setCurrentMood] = useState(moods[0]);
  const [isSpinning, setIsSpinning] = useState(false);
  const [showEmojis, setShowEmojis] = useState(false);

  const spinMood = () => {
    setIsSpinning(true);
    setShowEmojis(false);
    let spins = 0;
    const totalSpins = 20;
    const interval = setInterval(() => {
      setCurrentMood(moods[Math.floor(Math.random() * moods.length)]);
      spins++;
      if (spins >= totalSpins) {
        clearInterval(interval);
        setIsSpinning(false);
        setShowEmojis(true); // Trigger emoji animation when spinning stops
        setTimeout(() => setShowEmojis(false), 2000); // Hide emojis after 2 seconds
      }
    }, 100);
  };

  const handleGenerateAd = (segment) => {
    const prompt = generatePrompt(segment);
    alert(`Sending to ChatGPT API:\n\n${prompt}`);
    // Here you would typically make the API call to ChatGPT
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-4 bg-gradient-to-br from-rose-100 via-violet-200 to-teal-100 relative">
      {/* Emoji Animation Layer */}
      <AnimatePresence>
        {showEmojis && (
          <motion.div
            className="fixed inset-0 pointer-events-none z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {[...Array(20)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute text-4xl"
                initial={{
                  opacity: 0,
                  scale: 0,
                  x: window.innerWidth / 2,
                  y: window.innerHeight / 2,
                }}
                animate={{
                  opacity: [0, 1, 0],
                  scale: [0, 1.5, 1],
                  x: [
                    window.innerWidth / 2,
                    window.innerWidth * Math.random(),
                    window.innerWidth * Math.random(),
                  ],
                  y: [
                    window.innerHeight / 2,
                    window.innerHeight * Math.random(),
                    window.innerHeight * Math.random(),
                  ],
                }}
                transition={{
                  duration: 2,
                  ease: "easeOut",
                  delay: i * 0.1,
                }}
              >
                {currentMood.emoji}
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      <h1 className="text-3xl font-bold mt-8 mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-800 to-gray-600">
        Customer Segments Dashboard
      </h1>
      <div className="w-full max-w-7xl flex  ml-32">
        {/* Left side - Circle diagram and Selected Segment Card */}
        <div className="w-1/2 relative flex items-center justify-center min-h-[500px] ">
          {/* Central Uber circle */}
          <motion.div 
            className="w-32 h-32 rounded-full bg-gradient-to-br from-black to-gray-800 text-white flex items-center justify-center text-xl font-bold shadow-lg z-10"
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{
              duration: 3,
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
                className={`absolute w-28 h-28 rounded-full bg-gradient-to-br ${segment.gradient} text-white border-2 border-white/20 shadow-md flex items-center justify-center text-center p-2 cursor-pointer backdrop-blur-sm `}
                initial={{ 
                  scale: 0,
                  x: 0,
                  y: 0,
                  opacity: 0
                }}
                animate={{ 
                  scale: 1,
                  x: x,
                  y: y,
                  opacity: 1
                }}
                transition={{
                  duration: 0.8,
                  delay: 0.2 + (index * 0.1),
                  ease: "easeOut"
                }}
                onClick={() => setSelectedSegment(segment)}
                whileHover={{ 
                  scale: 1.1,
                  transition: { duration: 0.2 }
                }}
                style={{
                  left: 'calc(50% - 56px)',
                  top: 'calc(50% - 56px)',
                }}
              >
                <span className="text-sm font-medium">{segment.name}</span>
              </motion.div>
            );
          })}
        </div>

        {/* Right side - Circular Card */}
        <div className="w-1/2 pl-8 flex items-center justify-center ml-20">
          {selectedSegment && (
            <motion.div
              initial={{ scale: 0, y: 100, opacity: 0 }}
              animate={{ scale: 1, y: 0, opacity: 1 }}
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

        {/* Right side - Empty space for future content */}
        <div className="w-1/2 pl-8 flex items-center justify-center">
          {/* This space is now empty for future content */}
        </div>
      </div>

      {/* Mood Slot Machine - remains unchanged */}
      <motion.div
        className="fixed bottom-8 right-8 bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 border-2 border-white/20"
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 1, duration: 0.5 }}
      >
        <div className="flex flex-col items-center gap-4">
          <h3 className="text-xl font-bold text-gray-800">I'm Feeling...</h3>
          
          {/* Slot Machine Display */}
          <motion.div
            className="relative w-48 h-16 bg-gray-100 rounded-lg overflow-hidden border-2 border-gray-200 flex items-center justify-center"
            animate={{
              boxShadow: isSpinning 
                ? ["0 0 20px rgba(0,0,0,0.1)", "0 0 40px rgba(0,0,0,0.2)", "0 0 20px rgba(0,0,0,0.1)"]
                : "0 0 20px rgba(0,0,0,0.1)"
            }}
            transition={{ duration: 0.5, repeat: isSpinning ? Infinity : 0 }}
          >
            <motion.div
              className={`text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${currentMood.gradient} flex items-center gap-2`}
              animate={{ 
                y: isSpinning ? [-20, 0, 20] : 0,
                opacity: isSpinning ? [0.5, 1, 0.5] : 1
              }}
              transition={{ 
                duration: 0.2,
                repeat: isSpinning ? Infinity : 0
              }}
            >
              <span>{currentMood.emoji}</span>
              <span>{currentMood.text}</span>
            </motion.div>
          </motion.div>

          {/* Slot Machine Lever */}
          <motion.button
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-full font-bold shadow-lg flex items-center gap-2"
            onClick={spinMood}
            disabled={isSpinning}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span>Pull Lever</span>
            <span className="text-xl">🎰</span>
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}
