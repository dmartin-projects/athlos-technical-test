import React from 'react';
import HotelImages from './HotelImages';

const HotelDetailView = ({ hotel, onBack, loading }) => {
  if (loading) {
    return (
      <div className="hotel-detail-view">
        <div className="loading-detail">
          <p>Loading Hotel information...</p>
        </div>
      </div>
    );
  }

  if (!hotel) {
    return null;
  }

  return (
    <div className="hotel-detail-view">
      <div className="detail-header">
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
      </div>

      <div className="hotel-detail-content">
        <h1 className="detail-title">{hotel.name}</h1>
        
        <div className="detail-info-grid">
          <div className="detail-info-item">
            <strong>Location:</strong>
            <span>{hotel.location}</span>
          </div>
          
          <div className="detail-info-item">
            <strong>Average Price:</strong>
            <span>
              {hotel.average_price === 0 ? 
                <span className="price-not-available"> No price available for the selected dates</span> :
                `€${hotel.average_price}`
              }
            </span>
          </div>
          
          <div className="detail-info-item">
            <strong>Review Mark:</strong>
            <span>{hotel.review_mark}/10 ({hotel.comments} comentarios)</span>
          </div>
        </div>

        {hotel.description && (
          <div className="detail-description">
            <h3>Description</h3>
            <p>{hotel.description}</p>
          </div>
        )}

        {hotel.amenities && hotel.amenities.length > 0 && (
          <div className="detail-amenities">
            <h3>Services</h3>
            <div className="amenities-tags">
              {hotel.amenities.map((amenity, index) => (
                <span key={index} className="amenity-tag">
                  {amenity.name}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="detail-images">
          <h3>Gallery</h3>
          <HotelImages 
            images={hotel.photo_urls?.map(photo => photo.url) || []} 
            hotelName={hotel.name} 
          />
        </div>
      </div>
    </div>
  );
};

export default HotelDetailView;