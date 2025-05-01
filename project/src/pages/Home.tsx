import React, { useState, useRef, useEffect } from 'react';
import { Upload, Image as ImageIcon, Wand2, Download, Info, RefreshCw, Sparkles } from 'lucide-react';
import UploadZone from '../components/UploadZone';
import ProgressBar from '../components/ProgressBar';
import TexturePanel from '../components/TexturePanel';
import HowItWorks from '../components/HowItWorks';
import ShowcaseSlider from '../components/ShowcaseSlider';
import UserForm from '../components/UserForm';
import SegmentedImage from '../components/SegmentedImage';
import axios from 'axios';

function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showHowItWorks, setShowHowItWorks] = useState(false);
  const [segmentationData, setSegmentationData] = useState<any>(null);
  const [hoveredMaterial, setHoveredMaterial] = useState<{ id: number; name: string } | null>(null);
  const [hoveredMaterialTextures, setHoveredMaterialTextures] = useState<any[]>([]);
  const [selectedTextures, setSelectedTextures] = useState<any[]>([]);
  const [currentMask, setCurrentMask] = useState<any>(null);
  const segmentedImageRef = useRef<any>(null);

  const steps = [
    { title: 'Upload Image', icon: Upload },
    { title: 'Segment Parts', icon: ImageIcon },
    { title: 'Generate Textures', icon: Wand2 },
    { title: 'Download Result', icon: Download },
  ];

  const showcaseItems = [
    {
      before: "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=800&h=600&fit=crop",
      after: "https://images.unsplash.com/photo-1565374395542-0ce18882c857?w=800&h=600&fit=crop",
      title: "Modern Sofa",
      description: "From classic fabric to premium leather"
    },
    {
      before: "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=800&h=600&fit=crop",
      after: "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=800&h=600&fit=crop",
      title: "Dining Chair",
      description: "Traditional wood to velvet finish"
    },
    {
      before: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&h=600&fit=crop",
      after: "https://images.unsplash.com/photo-1550226891-ef816aed4a98?w=800&h=600&fit=crop",
      title: "Accent Chair",
      description: "Cotton blend to premium suede"
    }
  ];

  const handleImageUpload = (file: File) => {
    setSelectedImage(file);
    setCurrentStep(1);
    setIsProcessing(true);
  };

  const handleSegmentationComplete = (data: any) => {
    setSegmentationData(data);
    setIsProcessing(false);
    setCurrentStep(2);
  };

  const handleMaterialHover = (material: any) => {
    console.log('Home - handleMaterialHover called with:', material);
    setHoveredMaterial(material);
  };

  const handleMaskSelect = (mask: any) => {
    console.log('Home - handleMaskSelect:', mask);
    setCurrentMask(mask);
  };

  const handleTextureSelect = async (texture: any) => {
    debugger;
    console.log('Home - handleTextureSelect called:', {
      texture,
      currentMask,
      hasSegmentationData: !!segmentationData
    });
    
    if (!currentMask || !segmentationData) {
      console.warn('Please select a material on the image first');
      return;
    }

    // Add the selected texture to the selectedTextures array
    setSelectedTextures(prev => {
      // Remove any existing texture for this mask class
      const filtered = prev.filter(t => t.maskClass !== currentMask.class);
      // Add the new texture with mask class information
      return [...filtered, { ...texture, maskClass: currentMask.class }];
    });

    try {
      console.log('Home - Sending texture generation request:', {
        segmentationData,
        textureDescription: texture.description,
        maskClass: currentMask.class,
        prompt: texture.prompt || `Generate a seamless texture for ${currentMask.class} with these characteristics: ${texture.description}`
      });

      const response = await axios.post('http://localhost:5000/api/generate-texture', {
        segmentationData: segmentationData,
        textureDescription: texture.description,
        maskClass: currentMask.class,
        prompt: texture.prompt || `Generate a seamless texture for ${currentMask.class} with these characteristics: ${texture.description}`
      }, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('Home - Texture generation response:', response.data);

      if (response.data.success) {
        console.log('Home - Applying texture to mask');
        if (segmentedImageRef.current) {
          segmentedImageRef.current.applyTextureToMask(texture, currentMask, response.data.generatedTexture);
        } else {
          console.warn('Home - segmentedImageRef.current is null');
        }
      }
    } catch (error) {
      console.error('Home - Error generating texture:', error);
    }
  };

  useEffect(() => {
    console.log('Home - onTextureOptionsChange callback:', setHoveredMaterialTextures);
  }, []);

  useEffect(() => {
    console.log('Home - hoveredMaterialTextures updated:', hoveredMaterialTextures);
  }, [hoveredMaterialTextures]);

  return (
    <>
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-black opacity-50"></div>
        </div>
        
        {/* Hero Content */}
        <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Transform Your Designs with
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
              AI-Powered Textures
            </span>
          </h2>
          <p className="text-xl text-gray-300 mb-12">
            Upload any image and watch as our AI transforms it with stunning, realistic textures in seconds.
          </p>
        </div>

        {/* Main Content */}
        <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Panel - Upload and Preview */}
            <div className="lg:col-span-2 space-y-6">
              <div className="glass-effect rounded-2xl p-6 border border-white/20">
                <ProgressBar steps={steps} currentStep={currentStep} />
              </div>
              
              <div className="glass-effect rounded-2xl p-6 border border-white/20">
                {!selectedImage ? (
                  <UploadZone onUpload={handleImageUpload} />
                ) : (
                  <div className="space-y-4">
                    <SegmentedImage 
                      ref={segmentedImageRef}
                      imageFile={selectedImage} 
                      onSegmentationComplete={handleSegmentationComplete}
                      onMaterialHover={handleMaterialHover}
                      onTextureOptionsChange={setHoveredMaterialTextures}
                      onTextureSelect={handleTextureSelect}
                      onMaskSelect={handleMaskSelect}
                    />
                    {segmentationData && (
                      <div className="flex flex-wrap gap-2 mt-4">
                        {segmentationData.masks.map((mask: any, index: number) => (
                          <div
                            key={index}
                            className="px-3 py-1 rounded-full text-sm"
                            style={{
                              backgroundColor: `rgba(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]}, 0.2)`,
                              border: `1px solid rgb(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]})`,
                              color: `rgb(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]})`
                            }}
                          >
                            {mask.class}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Right Panel - Texture Options */}
            <div className="lg:col-span-1">
              <TexturePanel 
                isActive={currentStep >= 2} 
                hoveredMaterialTextures={hoveredMaterialTextures}
                selectedTextures={selectedTextures}
                onTextureSelect={handleTextureSelect}
                currentMask={currentMask}
              />
            </div>
          </div>
        </main>

        {/* Showcase Section */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
          <h3 className="text-2xl font-bold text-white text-center mb-12">
            See the Magic in Action
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {showcaseItems.map((item, index) => (
              <ShowcaseSlider
                key={index}
                before={item.before}
                after={item.after}
                title={item.title}
                description={item.description}
              />
            ))}
          </div>
        </div>
      </div>

      {/* How it Works Modal */}
      {showHowItWorks && <HowItWorks onClose={() => setShowHowItWorks(false)} />}
    </>
  );
}

export default Home;