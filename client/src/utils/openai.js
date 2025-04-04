import OpenAI from 'openai';

// Initialize the OpenAI client
const openai = new OpenAI({
  apiKey: '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',
  dangerouslyAllowBrowser: true // Only use this for development/demos
});

class OpenAIUtils {
  /**
   * Generate an engaging advertisement prompt for a merchant targeting a specific customer segment.
   * 
   * @param {string} merchantName - The name of the merchant
   * @param {Object} segment - An object with 'name' and 'description' attributes
   * @param {string} productName - The name of the product to advertise
   * @returns {Promise<string>} - The generated advertisement prompt
   */
  static async generateAdPrompt(merchantName, segment, productName) {
    const systemPrompt = `
You are a professional designer and marketer tasked with creating a hyper-specific advertisement image for ${merchantName}'s ${productName}. 
Your goal is to create a compelling visual that deeply resonates with the ${segment.name} customer segment while authentically representing ${merchantName}'s brand identity.
`;

    const userPrompt = `Create a photorealistic advertisement image for ${merchantName}'s ${productName} specifically designed to appeal to the following customer segment:

**Target Segment:** ${segment.name}
**Target Segment Details:** ${segment.description}

**Brand and Product Emphasis:**
- The image must be immediately recognizable as an advertisement for ${merchantName}
- The ${productName} must be the unmistakable focal point of the composition, with dramatic emphasis (spotlight effect, hero positioning, or visual framing)
- Incorporate subtle brand elements like ${merchantName}'s signature colors, aesthetic, or visual style without adding logos or text
- Create a "hero shot" of the product that captures its most appealing features from an optimal angle

**Product Presentation:**
- Position the ${productName} prominently in the foreground, ensuring it occupies at least 40% of the frame
- Show the product being used in a way that solves a problem or fulfills a need specifically relevant to ${segment.name}
- Include subtle environmental/contextual clues that signal this product is made for this specific audience
- Ensure product details are clearly visible with perfect lighting to highlight texture, materials, and key features

**Visual Details:**
- Setting: Place the product in an environment where ${segment.name} would naturally use it
- Props: Include 2-3 complementary objects that ${segment.name} would typically own or use, positioned to draw attention to the product
- Human element: Include a person representing the target segment actively engaging with the product, showing clear emotional benefit
- Perspective: Choose a camera angle that creates visual drama while highlighting the product's key features most relevant to this segment

**Technical Specifications:**
- Style: High-end advertising photography with cinematic quality, 8k resolution, professional product photography
- Lighting: Dramatic product highlighting with intentional light sources that create depth and make the product "pop" against the background
- Color palette: Use a limited color palette that emphasizes ${merchantName}'s brand colors, with complementary tones that make the product stand out
- Composition: Follow advertising industry best practices with the product as the clear hero, using visual flow to guide the eye directly to it
- Depth of field: Use selective focus to emphasize the product while creating atmospheric depth in the background

**Mood and Emotional Response:**
- The image should immediately convey the premium/quality nature of ${merchantName}'s offerings
- Evoke feelings of desire, trust, and excitement
- Create a sense of aspiration that makes the viewer want to own or experience the product

**Do NOT include:**
- Text overlays or logos (these will be added separately)
- Generic stock photo aesthetics
- Competing products or distracting elements
- Unrealistic or exaggerated product capabilities

Ensure the final image is instantly recognizable as a professional advertisement for ${merchantName}'s ${productName}, with the product dramatically highlighted and positioned as the unquestionable star of the composition while still creating an immediate connection with the ${segment.name} segment.`;
    
    try {
      const response = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt }
        ],
        response_format: { type: "text" }
      });
      
      return response.choices[0].message.content;
    } catch (error) {
      console.error(`Error generating ad prompt: ${error.message}`);
      throw error;
    }
  }

  /**
   * Fallback method that returns mock data when the API is unavailable
   * This can be useful for development or when you don't want to make actual API calls
   * 
   * @param {Object} segment - An object with 'name' and 'description' attributes
   * @returns {string} - Mock generated advertisement prompt
   */
  static generateMockAdPrompt(segment) {
    return `
      Visual Description:
      A vibrant image showing a diverse group of ${segment.name.toLowerCase()} using products in their daily lives, with elements reflecting ${segment.description.split('.')[0].toLowerCase()}.

      Headline:
      Perfect for ${segment.name}: Experience the Difference

      Caption:
      Designed for your lifestyle. Perfect for your needs. Experience the difference today! ✨

      Call to Action:
      Shop now and enjoy 20% off with code: ${segment.name.replace(/\s+/g, '').toUpperCase()}
    `;
  }
}

export default OpenAIUtils; 