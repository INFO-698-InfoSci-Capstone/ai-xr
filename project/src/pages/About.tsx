import React from 'react';
import { Users, Brain, Sparkles, Award } from 'lucide-react';

const About = () => {
  return (
    <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-white mb-6">About TextureAI</h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          We're revolutionizing the way designers and artists transform their creations
          using cutting-edge AI technology.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
        <div className="glass-effect rounded-2xl p-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-4">Our Mission</h2>
          <p className="text-gray-300">
            To empower creators with AI-powered tools that make texture transformation
            accessible, intuitive, and revolutionary. We believe in pushing the boundaries
            of what's possible in design and visualization.
          </p>
        </div>

        <div className="glass-effect rounded-2xl p-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-4">Our Vision</h2>
          <p className="text-gray-300">
            To become the leading platform for AI-powered texture transformation,
            serving creators worldwide with tools that bring their imagination to life
            in seconds.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div className="glass-effect rounded-2xl p-6 border border-white/20 text-center">
          <Users className="h-12 w-12 text-purple-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Team of Experts</h3>
          <p className="text-gray-300">
            Led by industry professionals with years of experience in AI and design.
          </p>
        </div>

        <div className="glass-effect rounded-2xl p-6 border border-white/20 text-center">
          <Brain className="h-12 w-12 text-blue-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Advanced AI</h3>
          <p className="text-gray-300">
            Powered by state-of-the-art machine learning models for optimal results.
          </p>
        </div>

        <div className="glass-effect rounded-2xl p-6 border border-white/20 text-center">
          <Sparkles className="h-12 w-12 text-pink-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Innovation</h3>
          <p className="text-gray-300">
            Constantly evolving our technology to provide cutting-edge solutions.
          </p>
        </div>

        <div className="glass-effect rounded-2xl p-6 border border-white/20 text-center">
          <Award className="h-12 w-12 text-green-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Quality First</h3>
          <p className="text-gray-300">
            Committed to delivering the highest quality results for our users.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;