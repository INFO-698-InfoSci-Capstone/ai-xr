import React from 'react';
import { X, Upload, ImageIcon, Wand2, Download } from 'lucide-react';

interface HowItWorksProps {
  onClose: () => void;
}

const HowItWorks: React.FC<HowItWorksProps> = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="glass-effect rounded-2xl max-w-2xl w-full p-8 border border-white/20">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold text-white">How it Works</h2>
          <button
            onClick={onClose}
            className="text-white/60 hover:text-white transition-colors duration-200"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="space-y-8">
          <div className="flex items-start space-x-6">
            <div className="bg-white/10 p-4 rounded-xl">
              <Upload className="h-8 w-8 text-purple-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">
                1. Upload Your Image
              </h3>
              <p className="text-white/70">
                Start by uploading an image of your object. We support common image
                formats like PNG and JPG.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-6">
            <div className="bg-white/10 p-4 rounded-xl">
              <ImageIcon className="h-8 w-8 text-blue-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">
                2. Instance Segmentation
              </h3>
              <p className="text-white/70">
                Our AI model analyzes your image and automatically identifies
                different parts of the object that can be retextured.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-6">
            <div className="bg-white/10 p-4 rounded-xl">
              <Wand2 className="h-8 w-8 text-pink-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">
                3. Texture Generation
              </h3>
              <p className="text-white/70">
                For each identified part, we generate multiple texture options using
                advanced AI algorithms. You can preview and select your preferred
                textures.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-6">
            <div className="bg-white/10 p-4 rounded-xl">
              <Download className="h-8 w-8 text-green-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">
                4. Download & Share
              </h3>
              <p className="text-white/70">
                Once you're happy with the results, download your retextured image or
                share it directly with others.
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={onClose}
          className="mt-8 w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 px-4 rounded-xl hover:opacity-90 transition-opacity duration-200 font-medium"
        >
          Got it!
        </button>
      </div>
    </div>
  );
};

export default HowItWorks;