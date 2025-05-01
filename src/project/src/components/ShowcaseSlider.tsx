import React, { useState, useRef, useEffect } from 'react';

interface ShowcaseSliderProps {
  before: string;
  after: string;
  title: string;
  description: string;
}

const ShowcaseSlider: React.FC<ShowcaseSliderProps> = ({
  before,
  after,
  title,
  description,
}) => {
  const [sliderPosition, setSliderPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);

  const handleMove = (event: MouseEvent | TouchEvent) => {
    if (!isDragging.current || !containerRef.current) return;

    const containerRect = containerRef.current.getBoundingClientRect();
    const x = 'touches' in event ? event.touches[0].clientX : event.clientX;
    const position = ((x - containerRect.left) / containerRect.width) * 100;
    setSliderPosition(Math.min(Math.max(position, 0), 100));
  };

  const handleMouseDown = () => {
    isDragging.current = true;
  };

  const handleMouseUp = () => {
    isDragging.current = false;
  };

  useEffect(() => {
    window.addEventListener('mousemove', handleMove);
    window.addEventListener('mouseup', handleMouseUp);
    window.addEventListener('touchmove', handleMove);
    window.addEventListener('touchend', handleMouseUp);

    return () => {
      window.removeEventListener('mousemove', handleMove);
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('touchmove', handleMove);
      window.removeEventListener('touchend', handleMouseUp);
    };
  }, []);

  return (
    <a href="#" className="showcase-link" onClick={(e) => e.preventDefault()}>
      <div className="showcase-item glass-effect rounded-2xl overflow-hidden">
        <div
          ref={containerRef}
          className="relative h-64 cursor-ew-resize group"
          onMouseDown={handleMouseDown}
          onTouchStart={handleMouseDown}
        >
          <img
            src={before}
            alt="Before"
            className="absolute inset-0 w-full h-full object-cover"
          />
          <div
            className="absolute inset-0 overflow-hidden"
            style={{ width: `${sliderPosition}%` }}
          >
            <img
              src={after}
              alt="After"
              className="absolute inset-0 w-full h-full object-cover"
            />
          </div>
          <div
            className="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize"
            style={{ left: `${sliderPosition}%` }}
          >
            <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center">
              <div className="w-1 h-4 bg-gray-400 rounded-full"></div>
            </div>
          </div>
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4">
            <span className="text-white text-sm font-medium">Drag to compare</span>
          </div>
        </div>
        <div className="p-4">
          <h3 className="text-lg font-semibold text-white mb-1">{title}</h3>
          <p className="text-white/70 text-sm">{description}</p>
        </div>
      </div>
    </a>
  );
};

export default ShowcaseSlider;