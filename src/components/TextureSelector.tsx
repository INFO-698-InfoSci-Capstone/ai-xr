import React, { useState, useEffect } from 'react';
import { Info } from 'lucide-react';

interface Texture {
  id: number;
  name: string;
  previewImage: string;
  description: string;
  category: string;
  thumbnail?: string;
  partName?: string;
}

interface TextureSelectorProps {
  furnitureTypeId: number;
  partId: number;
  onSelect: (textureId: number) => void;
}

const TextureSelector: React.FC<TextureSelectorProps> = ({ furnitureTypeId, partId, onSelect }) => {
  const [textures, setTextures] = useState<Texture[]>([]);
  const [selectedTexture, setSelectedTexture] = useState<number | null>(null);
  const [hoveredTexture, setHoveredTexture] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTextures = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/api/texture-options?furniture_type_id=${furnitureTypeId}&part_id=${partId}`);
        const data = await response.json();
        
        if (data.success) {
          const transformedTextures = data.data.map((texture: any) => ({
            id: texture.id,
            name: texture.name,
            previewImage: texture.previewImage || texture.preview_image_path,
            description: texture.description,
            category: texture.category,
            thumbnail: texture.thumbnail || texture.thumbnail_path,
            partName: texture.partName
          }));
          
          setTextures(transformedTextures);
          setSelectedTexture(null); // Reset selection when textures change
        } else {
          setError(data.error || 'Failed to load textures');
        }
      } catch (error) {
        console.error('Error fetching textures:', error);
        setError('Error loading textures');
      } finally {
        setLoading(false);
      }
    };

    if (furnitureTypeId && partId) {
      fetchTextures();
    }
  }, [furnitureTypeId, partId]);

  const handleTextureSelect = (textureId: number) => {
    setSelectedTexture(textureId);
    onSelect(textureId);
  };

  if (loading) {
    return <div className="text-white text-center py-4">Loading textures...</div>;
  }

  if (error) {
    return <div className="text-white text-center py-4 bg-red-500/20 rounded-lg">{error}</div>;
  }

  return (
    <div className="w-full">
      <div className="grid grid-cols-2 gap-4">
        {textures.length === 0 ? (
          <div className="col-span-2 text-center text-white py-4">
            No textures available for this part
          </div>
        ) : (
          textures.map((texture) => (
            <div
              key={texture.id}
              className="relative"
              onMouseEnter={() => setHoveredTexture(texture.id)}
              onMouseLeave={() => setHoveredTexture(null)}
            >
              <label
                className={`block relative rounded-xl overflow-hidden cursor-pointer transition-all duration-200 hover:scale-105 ${
                  selectedTexture === texture.id
                    ? 'ring-4 ring-white'
                    : 'ring-2 ring-white/30'
                }`}
              >
                <input
                  type="radio"
                  name="texture"
                  value={texture.id}
                  checked={selectedTexture === texture.id}
                  onChange={() => handleTextureSelect(texture.id)}
                  className="sr-only"
                />
                <div className="aspect-square bg-white/20">
                  <img
                    src={texture.previewImage}
                    alt={texture.name}
                    className="w-full h-full object-cover opacity-80 hover:opacity-100 transition-opacity duration-200"
                  />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/0 to-black/0">
                  <div className="absolute bottom-0 left-0 right-0 p-3">
                    <p className="text-white text-sm font-medium">
                      {texture.name}
                    </p>
                    <p className="text-white/70 text-xs">
                      {texture.category}
                    </p>
                  </div>
                </div>
              </label>

              {hoveredTexture === texture.id && (
                <div className="absolute z-50 w-64 p-4 bg-black/90 rounded-xl shadow-xl -translate-y-full -translate-x-1/4 top-0 left-1/2 mt-[-10px]">
                  <div className="flex items-start space-x-2">
                    <Info className="w-5 h-5 text-pink-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-white">{texture.name}</h4>
                      <p className="text-sm text-gray-300 mt-1">
                        {texture.description}
                      </p>
                      {texture.partName && (
                        <p className="text-sm text-pink-400 mt-1">
                          Compatible with: {texture.partName}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 rotate-45 w-4 h-4 bg-black/90" />
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TextureSelector;