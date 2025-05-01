import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface TextureOptionsProps {
  selectedFurnitureType?: number;
  selectedPart?: number;
  hoveredMaterial: {
    id: number;
    name: string;
  }
  onTextureSelect: (texture: TextureOption) => void;
  selectedTexture?: TextureOption | null;
}

interface TextureOption {
  id: number;
  name: string;
  category: string;
  preview_image_path: string;
  thumbnail_path: string;
  description: string;
}

const TextureOptions: React.FC<TextureOptionsProps> = ({
  
  selectedFurnitureType,
  selectedPart,
  hoveredMaterial,
  onTextureSelect,
  selectedTexture
}) => {
  debugger;
  console.log('TextureOptions - received onTextureSelect prop:', Boolean(onTextureSelect));
  const [textureOptions, setTextureOptions] = useState<TextureOption[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTextureOptions = async () => {
      try {
        setError(null);
        const params: any = {};
        
        if (hoveredMaterial) {
          params.material_type = hoveredMaterial.name;
        } else {
          if (selectedFurnitureType) params.furniture_type_id = selectedFurnitureType;
          if (selectedPart) params.part_id = selectedPart;
        }

        const response = await axios.get('http://localhost:5000/api/texture-options', { params });
        
        if (response.data.success) {
          setTextureOptions(response.data.data);
        }
      } catch (error) {
        console.error('Error fetching texture options:', error);
        setError('Failed to load texture options');
      }
    };

    fetchTextureOptions();
  }, [selectedFurnitureType, selectedPart, hoveredMaterial]);

  const getImageUrl = (path: string) => {
    const cleanPath = path.replace(/^\/+/, '');
    return `http://localhost:5000/${cleanPath}`;
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="p-4 text-center">
          <p>Loading textures...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="p-4 text-center">
          <p className="text-red-500">Error: {error}</p>
        </div>
      );
    }

    if (!textureOptions.length) {
      return (
        <div className="p-4 text-center">
          <p>
            {hoveredMaterial 
              ? `No textures available for ${hoveredMaterial.name}`
              : selectedFurnitureType && selectedPart
                ? 'No textures available for the selected furniture and part'
                : 'Select a furniture type and part or hover over a material'}
          </p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {textureOptions.map((texture) => (
          <div
            key={texture.id}
            onClick={() => {
              console.log('Texture clicked:', texture);
              if (onTextureSelect) onTextureSelect(texture);
            }}
            className={`cursor-pointer border-2 ${
              selectedTexture?.id === texture.id ? 'border-blue-500' : 'border-transparent'
            } rounded-md overflow-hidden transition-all duration-200 hover:scale-105 hover:shadow-md bg-white`}
          >
            {/* ... */}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm">
      <h2 className="text-lg font-bold mb-2">
        {hoveredMaterial 
          ? `${hoveredMaterial.name} Textures`
          : 'Available Textures'}
      </h2>
      {renderContent()}
    </div>
  );
};

export default TextureOptions; 