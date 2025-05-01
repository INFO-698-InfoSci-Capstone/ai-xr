import React, { useState } from 'react';
import { Mail, MessageSquare, Phone, MapPin } from 'lucide-react';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log('Form submitted:', formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-white mb-6">Contact Us</h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          Have questions? We're here to help. Reach out to our team and we'll get back to you as soon as possible.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="glass-effect rounded-2xl p-8 border border-white/20">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-white mb-2">
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Your name"
                  required
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-white mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="your@email.com"
                  required
                />
              </div>

              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-white mb-2">
                  Subject
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="How can we help?"
                  required
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-medium text-white mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  rows={6}
                  className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Your message..."
                  required
                />
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 px-4 rounded-xl hover:opacity-90 transition-opacity duration-200 font-medium"
              >
                Send Message
              </button>
            </form>
          </div>
        </div>

        <div className="space-y-6">
          <div className="glass-effect rounded-2xl p-6 border border-white/20">
            <div className="flex items-center space-x-4">
              <Mail className="h-6 w-6 text-purple-400" />
              <div>
                <h3 className="text-lg font-medium text-white">Email</h3>
                <p className="text-gray-300">support@textureai.com</p>
              </div>
            </div>
          </div>

          <div className="glass-effect rounded-2xl p-6 border border-white/20">
            <div className="flex items-center space-x-4">
              <Phone className="h-6 w-6 text-blue-400" />
              <div>
                <h3 className="text-lg font-medium text-white">Phone</h3>
                <p className="text-gray-300">+1 (555) 123-4567</p>
              </div>
            </div>
          </div>

          <div className="glass-effect rounded-2xl p-6 border border-white/20">
            <div className="flex items-center space-x-4">
              <MapPin className="h-6 w-6 text-pink-400" />
              <div>
                <h3 className="text-lg font-medium text-white">Location</h3>
                <p className="text-gray-300">San Francisco, CA</p>
              </div>
            </div>
          </div>

          <div className="glass-effect rounded-2xl p-6 border border-white/20">
            <div className="flex items-center space-x-4">
              <MessageSquare className="h-6 w-6 text-green-400" />
              <div>
                <h3 className="text-lg font-medium text-white">Live Chat</h3>
                <p className="text-gray-300">Available 24/7</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;