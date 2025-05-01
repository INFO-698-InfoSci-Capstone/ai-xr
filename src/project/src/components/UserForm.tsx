import React, { useState } from 'react';

interface FormData {
  category: string;
  name: string;
  email: string;
  company?: string;
  studentId?: string;
  interests: string[];
  experience: string;
  notifications: boolean;
}

const UserForm = () => {
  const [formData, setFormData] = useState<FormData>({
    category: '',
    name: '',
    email: '',
    interests: [],
    experience: '',
    notifications: false,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checkbox = e.target as HTMLInputElement;
      if (name === 'notifications') {
        setFormData(prev => ({ ...prev, [name]: checkbox.checked }));
      } else if (name === 'interests') {
        const updatedInterests = checkbox.checked
          ? [...formData.interests, value]
          : formData.interests.filter(interest => interest !== value);
        setFormData(prev => ({ ...prev, interests: updatedInterests }));
      }
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
  };

  return (
    <div className="glass-effect rounded-2xl p-8 border border-white/20">
      <h3 className="text-2xl font-bold text-white mb-6">Get Started</h3>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-white mb-2">
            I am a...
          </label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          >
            <option value="">Select category</option>
            <option value="student">Student</option>
            <option value="professional">Professional</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Name
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Your name"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Email
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="your@email.com"
              required
            />
          </div>
        </div>

        {formData.category === 'professional' && (
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Company
            </label>
            <input
              type="text"
              name="company"
              value={formData.company || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Company name"
            />
          </div>
        )}

        {formData.category === 'student' && (
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Student ID
            </label>
            <input
              type="text"
              name="studentId"
              value={formData.studentId || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Student ID"
            />
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-white mb-2">
            Interests
          </label>
          <div className="space-y-2">
            {['Interior Design', 'Architecture', 'Product Design', 'Fashion'].map((interest) => (
              <label key={interest} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="interests"
                  value={interest}
                  checked={formData.interests.includes(interest)}
                  onChange={handleChange}
                  className="rounded border-white/20 bg-white/10 text-purple-600 focus:ring-purple-500"
                />
                <span className="text-white">{interest}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-white mb-2">
            Experience Level
          </label>
          <div className="space-x-4">
            {['Beginner', 'Intermediate', 'Advanced'].map((level) => (
              <label key={level} className="inline-flex items-center">
                <input
                  type="radio"
                  name="experience"
                  value={level.toLowerCase()}
                  checked={formData.experience === level.toLowerCase()}
                  onChange={handleChange}
                  className="border-white/20 bg-white/10 text-purple-600 focus:ring-purple-500"
                />
                <span className="ml-2 text-white">{level}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              name="notifications"
              checked={formData.notifications}
              onChange={handleChange}
              className="rounded border-white/20 bg-white/10 text-purple-600 focus:ring-purple-500"
            />
            <span className="text-white">Receive notifications about new features and updates</span>
          </label>
        </div>

        <button
          type="submit"
          className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 px-4 rounded-xl hover:opacity-90 transition-opacity duration-200 font-medium"
        >
          Get Started
        </button>
      </form>
    </div>
  );
};

export default UserForm;