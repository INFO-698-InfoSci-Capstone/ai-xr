import React, { useState, useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import axios from 'axios';

interface MaterialCategory {
  id: number;
  name: string;
}

interface SegmentedImageProps {
  imageFile: File;
  onSegmentationComplete?: (data: any) => void;
  onMaterialHover: (material: { id: number; name: string } | null) => void;
  onTextureOptionsChange?: (options: any[]) => void;
  onTextureSelect: (texture: any) => void;
  onMaskSelect?: (mask: any) => void;
  furnitureTypeId?: number;
}

// Add axios default configuration
axios.defaults.withCredentials = true;

const SegmentedImage = forwardRef<any, SegmentedImageProps>(({
  imageFile,
  onSegmentationComplete,
  onMaterialHover,
  onTextureOptionsChange,
  onTextureSelect,
  onMaskSelect,
  furnitureTypeId
}, ref) => {
  const [segmentationData, setSegmentationData] = useState<any>(null);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [hoveredClass, setHoveredClass] = useState<string | null>(null);
  const [selectedMask, setSelectedMask] = useState<any>(null);
  const [appliedTextures, setAppliedTextures] = useState<Record<string, any>>({});
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  useImperativeHandle(ref, () => ({
    applyTextureToMask: (texture: any, mask: any, generatedTexture: string) => {
      console.log('DEBUG: applyTextureToMask function called');
      if (texture && mask) {
        setAppliedTextures(prev => ({
          ...prev,
          [mask.class]: {
            texture: texture,
            generatedTexture: generatedTexture || null // Add fallback
          }
        }));
        drawSegmentation(hoveredClass);
      }
    }
  }));

  useEffect(() => {
    const url = URL.createObjectURL(imageFile);
    setImageUrl(url);

    const formData = new FormData();
    formData.append('file', imageFile);

    axios.post('http://localhost:5000/api/segment', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      withCredentials: true
    })
    .then(response => {
      if (response.data.success) {
        console.log('Segmentation response:', response.data);
        setSegmentationData(response.data);
        if (onSegmentationComplete) {
          onSegmentationComplete(response.data);
        }
      }
    })
    .catch(error => {
      console.error('Error processing image:', error);
    });

    return () => {
      URL.revokeObjectURL(url);
    };
  }, [imageFile, onSegmentationComplete]);

  /* Update the applyTextureToMask function to properly store segmented parts data*/
  const applyTextureToMask = async (texture: any, mask: any) => {
    console.log('DEBUG: applyTextureToMask function called');
    try {
      console.log('Applying texture:', texture);
      console.log('To mask:', mask);
      console.log('Segmentation data:', segmentationData);
      
      // Update the global hoveredMaterialTextures with the selected texture
      if (typeof window !== 'undefined') {
        (window as any).hoveredMaterialTextures = {
          ...(window as any).hoveredMaterialTextures,
          texture: texture
        };
      }
      
      // Create a properly structured segmentedParts object
      const segmentedParts = {
        [mask.class]: {
          id: mask.class,
          texture: texture,
          maskData: mask,
          textureDescription: texture.description,
          prompt: texture.prompt || `Generate a seamless texture for ${mask.class} with these characteristics: ${texture.description}`
        }
      };
      
      console.log('Sending segmentedParts to backend:', segmentedParts);
      
      const response = await axios.post('http://localhost:5000/api/generate-texture', {
        segmentationData: segmentationData,
        textureDescription: texture.description,
        maskClass: mask.class,
        segmentedParts: segmentedParts, // Add this structured data to the request
        prompt: texture.prompt || `Generate a seamless texture for ${mask.class} with these characteristics: ${texture.description}`
      }, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      console.log('Texture generation response:', response.data);
  
      if (response.data.success) {
        setAppliedTextures(prev => {
          console.log('Previous appliedTextures:', prev);
          
          // Create a new object (not a Map)
          const updated = {
            ...prev,
            [mask.class]: {
              texture: texture,
              generatedTexture: response.data.generatedTexture
            }
          };
          
          console.log('Updated appliedTextures:', updated);
          return updated;
        });
        //drawSegmentation(hoveredClass); //called by useEffect
      }
    } catch (error) {
      console.error('Error generating texture:', error);
    }
  };
  useEffect(() => {
    if (appliedTextures.size > 0) {
      console.log('appliedTextures changed:', Array.from(appliedTextures.entries()));
      drawSegmentation(hoveredClass);
    }
  }, [appliedTextures, hoveredClass]);


  // Update the handleTextureSelect function if you have one
  const handleTextureSelect = (texture: any) => {
    if (!selectedMask) {
      console.warn('No mask selected for texture application');
      return;
    }
    
    console.log('Texture selected:', texture);
    console.log('For mask:', selectedMask);
    
    // Apply the texture to the selected mask
    applyTextureToMask(texture, selectedMask);
  };

  const drawSegmentation = (hoverClass: string | null = null) => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx || !segmentationData?.masks) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    segmentationData.masks.forEach((mask: any) => {
      const points = mask.points;
      if (!points || points.length < 3) return;

      // Check if this is the hovered class
      const isHovered = hoverClass === mask.class;
      
      const appliedTexture = appliedTextures[mask.class];
      console.log(`For class ${mask.class}, appliedTexture:`, appliedTexture);

      ctx.beginPath();
      ctx.moveTo(points[0][0], points[0][1]);
      points.forEach((point: [number, number]) => ctx.lineTo(point[0], point[1]));
      ctx.closePath();

      if (appliedTexture && appliedTexture.generatedTexture) {
        console.log(`Drawing texture for ${mask.class}:`, appliedTexture.generatedTexture);
        
        // Create an image element for the texture
        const textureImg = new Image();
        
        // Important: Set up the onload handler BEFORE setting the src
        textureImg.onload = () => {
          console.log(`Texture image loaded for ${mask.class}`);
          
          // Need to redraw the path for clipping
          ctx.beginPath();
          ctx.moveTo(points[0][0], points[0][1]);
          for (let i = 1; i < points.length; i++) {
            ctx.lineTo(points[i][0], points[i][1]);
          }
          ctx.closePath();
          
          // Calculate bounds for the texture
          let minX = Infinity, minY = Infinity;
          let maxX = -Infinity, maxY = -Infinity;
          
          points.forEach((point: [number, number]) => {
            minX = Math.min(minX, point[0]);
            minY = Math.min(minY, point[1]);
            maxX = Math.max(maxX, point[0]);
            maxY = Math.max(maxY, point[1]);
          });
          
          const width = maxX - minX;
          const height = maxY - minY;
          
          // Apply clipping and draw the texture
          ctx.save();
          ctx.clip();
          ctx.drawImage(textureImg, minX, minY, width, height);
          ctx.restore();
          
          // Draw the outline again
          ctx.strokeStyle = `rgb(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]})`;
          ctx.lineWidth = 2;
          ctx.stroke();
        };
        
        // Add error handling
        textureImg.onerror = (e) => {
          console.error(`Error loading texture for ${mask.class}:`, e);
        };
        
        // Set crossOrigin to avoid CORS issues with image loading
        textureImg.crossOrigin = 'anonymous';
        
        // After handlers are set up, set the src to start loading
        textureImg.src = appliedTexture.generatedTexture;
      } else if (isHovered) {
          // Fill with semi-transparent color when hovering
          ctx.fillStyle = `rgba(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]}, 0.3)`;
          ctx.fill();
          
          // Show part label
          ctx.fillStyle = 'black';
          ctx.font = '14px Arial';
          ctx.fillText(mask.class, points[0][0], points[0][1] - 5);
      }

      // Draw outline
      ctx.strokeStyle = `rgb(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]})`;
      ctx.lineWidth = 2;
      ctx.stroke();
      });
    };

  const fetchTextureOptions = async (materialName: string) => {
    try {
      console.log('SegmentedImage - Fetching texture options for:', materialName);
      const response = await axios.get('http://localhost:5000/api/texture-options', {
        params: {
          material_type: materialName
        }
      });
      
      console.log('SegmentedImage - Texture options response:', response.data);
      if (response.data.success && onTextureOptionsChange) {
        onTextureOptionsChange(response.data.data);
      }
    } catch (error) {
      console.error('SegmentedImage - Error fetching texture options:', error);
    }
  };

  const handleMaskClick = (mask: any) => {
    console.log('SegmentedImage - handleMaskClick:', mask);
    setSelectedMask(mask);
    if (onMaskSelect) {
      onMaskSelect(mask);
    }
    
    // Update the hover state for visual highlighting
    handleClassHover(mask.class);
    
    // Create a global variable to store the current mask's material
    if (typeof window !== 'undefined') {
      (window as any).hoveredMaterialTextures = {
        materialId: mask.class,
        maskData: mask
      };
    }
    
    // Always fetch texture options when a mask is clicked
    if (mask.class && segmentationData?.material_categories) {
      const materialCategory = segmentationData.material_categories.find(
        (cat: MaterialCategory) => cat.name.toLowerCase() === mask.class.toLowerCase()
      );
      
      if (materialCategory) {
        console.log('SegmentedImage - Fetching textures for clicked mask:', materialCategory);
        fetchTextureOptions(materialCategory.name);
      }
    }
  };

  const handleClassHover = async (className: string | null) => {
    console.log('SegmentedImage - handleClassHover:', className);
    setHoveredClass(className);
    drawSegmentation(className);
    
    if (className && segmentationData?.material_categories) {
      // Find the material category for the hovered class
      const materialCategory = segmentationData.material_categories.find(
        (cat: MaterialCategory) => cat.name.toLowerCase() === className.toLowerCase()
      );
      
      if (materialCategory) {
        console.log('SegmentedImage - Found material category:', materialCategory);
        onMaterialHover(materialCategory);
        // Note: We've removed the fetchTextureOptions call from here
      } else {
        console.log('SegmentedImage - No material category found for:', className);
        onMaterialHover(null);
      }
    } else {
      onMaterialHover(null);
    }
  };

  useEffect(() => {
    if (imageUrl && segmentationData) {
      const img = imageRef.current;
      if (img) {
        img.onload = () => {
          if (canvasRef.current) {
            canvasRef.current.width = img.naturalWidth;
            canvasRef.current.height = img.naturalHeight;
            drawSegmentation(hoveredClass);
          }
        };
      }
    }
  }, [imageUrl, segmentationData, hoveredClass, appliedTextures]);

  return (
    <div className="space-y-4">
      <div 
        className="relative w-full"
        style={{ 
          maxWidth: '100%',
          aspectRatio: imageRef.current ? `${imageRef.current.naturalWidth} / ${imageRef.current.naturalHeight}` : 'auto'
        }}
      >
        <img
          ref={imageRef}
          src={imageUrl}
          alt="Uploaded furniture"
          className="absolute top-0 left-0 w-full h-full object-contain"
          style={{ opacity: 0.8 }}
          onLoad={(e) => {
            const img = e.target as HTMLImageElement;
            if (canvasRef.current) {
              // Set canvas size to match natural image dimensions
              canvasRef.current.width = img.naturalWidth;
              canvasRef.current.height = img.naturalHeight;
              drawSegmentation(hoveredClass);
            }
          }}
        />
        <canvas
          ref={canvasRef}
          className="absolute top-0 left-0 w-full h-full cursor-pointer"
          onClick={(e) => {
            const canvas = canvasRef.current;
            if (!canvas || !segmentationData?.masks) return;

            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate scale based on natural dimensions vs display dimensions
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            // Apply scaling to get the correct coordinates
            const px = x * scaleX;
            const py = y * scaleY;

            for (const mask of segmentationData.masks) {
              const ctx = canvas.getContext('2d');
              if (ctx) {
                ctx.beginPath();
                ctx.moveTo(mask.points[0][0], mask.points[0][1]);
                mask.points.forEach((point: number[]) => ctx.lineTo(point[0], point[1]));
                ctx.closePath();
                if (ctx.isPointInPath(px, py)) {
                  handleMaskClick(mask);
                  break;
                }
              }
            }
          }}
          onMouseMove={(e) => {
            const canvas = canvasRef.current;
            if (!canvas || !segmentationData?.masks) return;

            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate scale based on natural dimensions vs display dimensions
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            // Apply scaling to get the correct coordinates
            const px = x * scaleX;
            const py = y * scaleY;

            let foundClass = null;
            for (const mask of segmentationData.masks) {
              const ctx = canvas.getContext('2d');
              if (ctx) {
                ctx.beginPath();
                ctx.moveTo(mask.points[0][0], mask.points[0][1]);
                mask.points.forEach((point: number[]) => ctx.lineTo(point[0], point[1]));
                ctx.closePath();
                if (ctx.isPointInPath(px, py)) {
                  foundClass = mask.class;
                  break;
                }
              }
            }

            if (foundClass !== hoveredClass) {
              handleClassHover(foundClass);
            }
          }}
          onMouseLeave={() => handleClassHover(null)}
        />
      </div>
      
      {segmentationData && (
        <div className="flex flex-wrap gap-2">
          {segmentationData.masks.map((mask: any, index: number) => (
            <button
              key={index}
              className="px-3 py-1 rounded-full text-sm transition-all duration-200"
              style={{
                backgroundColor: hoveredClass === mask.class 
                  ? `rgba(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]}, 0.3)`
                  : `rgba(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]}, 0.1)`,
                border: `1px solid rgb(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]})`,
                color: `rgb(${mask.rgb_color[0]}, ${mask.rgb_color[1]}, ${mask.rgb_color[2]})`
              }}
              onClick={() => handleMaskClick(mask)}
              onMouseEnter={() => handleClassHover(mask.class)}
              onMouseLeave={() => handleClassHover(null)}
            >
              {mask.class}
              {appliedTextures[mask.class] && ' ✓'}
            </button>
          ))}
        </div>
      )}
    </div>
  );
});

export default SegmentedImage; 