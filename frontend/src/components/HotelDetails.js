import React from 'react';
import HotelImages from './HotelImages';

const HotelDetails = ({ hotelData, onSave, saving, onShowSavedHotels }) => {
  if (!hotelData) {
    return null;
  }


  return (
    <div className="hotel-details">
      <h2>{hotelData.name}</h2>
      
      <div className="hotel-info">
        <p><strong>Location:</strong> {hotelData.location || "No data found on the hotel's webpage"}</p>
        <p>
          <strong>Average Price:</strong> 
          {hotelData.average_price === 0.00 || hotelData.average_price === 0 ? 
            <span className="price-not-available"> No price available for the selected dates</span> : 
            ` €${hotelData.average_price}`
          }
        </p>
        <p><strong>Review Mark:</strong> {hotelData.review_mark || "No data found on the hotel's webpage"}/10 ({hotelData.comments || 0} comentarios)</p>
      </div>

      <div className="hotel-description">
        <strong>Description:</strong>
        <p>{hotelData.description || "No data found on the hotel's webpage"}</p>
      </div>

      {hotelData.amenities && hotelData.amenities.length > 0 && (
        <div className="hotel-amenities">
          <strong>Services:</strong>
          <p>{hotelData.amenities.join(', ')}</p>
        </div>
      )}

      <HotelImages 
        images={hotelData.photo_urls} 
        hotelName={hotelData.name} 
      />

      <div className="hotel-actions">
        <button
          onClick={async () => {
            const result = await onSave();
            if (result && onShowSavedHotels) {
              setTimeout(() => onShowSavedHotels(), 1500);
            }
          }}
          disabled={saving}
          className={`save-button ${saving ? 'saving' : ''}`}
        >
          {saving ? 'Saving...' : 'Save'}
        </button>
      </div>
    </div>
  );
};

export default HotelDetails;