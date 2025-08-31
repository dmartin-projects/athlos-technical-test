import React from 'react';
import { useHotelList } from '../hooks/useHotelList';
import HotelCard from './HotelCard';
import HotelDetailView from './HotelDetailView';
import './HotelList.css';

const HotelList = ({ onBackToSearch }) => {
  const {
    hotels,
    loading,
    error,
    selectedHotel,
    loadingDetail,
    deleting,
    fetchHotelDetail,
    deleteHotel,
    clearError,
    clearSelectedHotel
  } = useHotelList();

  const handleHotelClick = (hotelId) => {
    fetchHotelDetail(hotelId);
  };

  const handleBackToList = () => {
    clearSelectedHotel();
  };

  if (selectedHotel || loadingDetail) {
    return (
      <HotelDetailView
        hotel={selectedHotel}
        onBack={handleBackToList}
        loading={loadingDetail}
      />
    );
  }

  return (
    <div className="hotel-list-container">
      <div className="list-header">
        <h1>Saved Hotels</h1>
        <button className="back-to-search-button" onClick={onBackToSearch}>
          ← Back
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={clearError} className="close-error">×</button>
        </div>
      )}

      {loading ? (
        <div className="loading-hotels">
          <p>Loading hotels...</p>
        </div>
      ) : hotels.length === 0 ? (
        <div className="no-hotels">
          <p>Not found saved hotels.</p>
          <p>¡See your saved hotels!</p>
        </div>
      ) : (
        <div className="hotels-grid">
          {hotels.map((hotel) => (
            <HotelCard
              key={hotel.id}
              hotel={hotel}
              onClick={handleHotelClick}
              onDelete={deleteHotel}
              deleting={deleting}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default HotelList;