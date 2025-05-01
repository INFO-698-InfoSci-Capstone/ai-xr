import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Wand2 } from 'lucide-react';

const Navigation = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="relative z-10 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <Wand2 className="h-8 w-8 text-white" />
            <h1 className="text-2xl font-bold text-white">TextureAI</h1>
          </Link>
          <nav className="flex items-center space-x-6">
            <Link
              to="/"
              className={`text-sm font-medium transition-colors duration-200 ${
                isActive('/') ? 'text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              Home
            </Link>
            <Link
              to="/about"
              className={`text-sm font-medium transition-colors duration-200 ${
                isActive('/about') ? 'text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              About
            </Link>
            <Link
              to="/contact"
              className={`text-sm font-medium transition-colors duration-200 ${
                isActive('/contact') ? 'text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              Contact
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Navigation;