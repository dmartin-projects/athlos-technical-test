import React from 'react';

const HotelImages = ({ images, hotelName }) => {
  if (!images || images.length === 0) {
    return null;
  }

  const handleImageError = (e) => {
    e.target.style.display = 'none';
  };

  return (
    <div className="hotel-images">
      <strong>Image ({images.length}):</strong>
      <div className="images-grid">
        {images.map((url, index) => (
          <img
            key={index}
            src={url}
            alt={`${hotelName} ${index + 1}`}
            className="hotel-image"
            onError={handleImageError}
          />
        ))}
      </div>
    </div>
  );
};

export default HotelImages;