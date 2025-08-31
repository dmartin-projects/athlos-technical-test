import React, { useState } from 'react';

const HotelCard = ({ hotel, onClick, onDelete, deleting }) => {
  const [imageError, setImageError] = useState(false);

  const handleClick = () => {  
    onClick(hotel.id);
  };

  const handleDelete = (e) => {
    e.stopPropagation();
    onDelete(hotel.id);
  };

  const handleImageError = () => {
    setImageError(true);
  };

  const hasValidImage = hotel.photo_urls && hotel.photo_urls.length > 0 && !imageError;
  const isDeleting = deleting === hotel.id;

  return (
    <div className="hotel-card" onClick={handleClick}>
      <div className="hotel-card-image">
        {hasValidImage ? (
          <img 
            src={hotel.photo_urls[0].url} 
            alt={hotel.name}
            onError={handleImageError}
          />
        ) : (
          <div className="image-placeholder">
            <span className="placeholder-text">Image not found</span>
          </div>
        )}
      </div>
      
      <div className="hotel-card-content">
        <h3 className="hotel-card-title">{hotel.name}</h3>
        <p className="hotel-card-location">{hotel.location}</p>
        
        <div className="hotel-card-info">
          <span className="hotel-card-rating">
            {hotel.review_mark}/10
          </span>
          <span className="hotel-card-price">
            {hotel.average_price === 0 ? 
              <span className="price-not-available-small">No price</span> :
              `€${hotel.average_price}`
            }
          </span>
        </div>
        
        <button 
          className={`delete-button ${isDeleting ? 'deleting' : ''}`}
          onClick={handleDelete}
          disabled={isDeleting}
        >
          {isDeleting ? 'Deleting...' : 'X'}
        </button>
      </div>
    </div>
  );
};

export default HotelCard;