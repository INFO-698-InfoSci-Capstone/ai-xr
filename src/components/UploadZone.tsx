import React, { useCallback } from 'react';
import { Upload, FileImage } from 'lucide-react';

interface UploadZoneProps {
  onUpload: (file: File) => void;
}

const UploadZone: React.FC<UploadZoneProps> = ({ onUpload }) => {
  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        onUpload(file);
      }
    },
    [onUpload]
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className="border-2 border-dashed border-white/30 rounded-xl p-12 text-center hover:border-white/50 transition-colors duration-200"
    >
      <input
        type="file"
        accept="image/*"
        onChange={handleFileInput}
        className="hidden"
        id="file-upload"
      />
      <label
        htmlFor="file-upload"
        className="cursor-pointer flex flex-col items-center"
      >
        <div className="relative">
          <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 blur"></div>
          <div className="relative bg-black/30 p-4 rounded-full">
            <Upload className="h-12 w-12 text-white" />
          </div>
        </div>
        <p className="text-xl font-medium text-white mt-6 mb-2">
          Drop your image here
        </p>
        <p className="text-white/70">or click to upload</p>
        <div className="mt-6 flex items-center justify-center space-x-4 text-sm text-white/50">
          <div className="flex items-center">
            <FileImage className="h-4 w-4 mr-2" />
            <span>PNG, JPG</span>
          </div>
          <div className="w-1 h-1 rounded-full bg-white/30"></div>
          <span>Up to 10MB</span>
        </div>
      </label>
    </div>
  );
};

export default UploadZone;