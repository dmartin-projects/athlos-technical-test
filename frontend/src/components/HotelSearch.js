import React from 'react';
import { useHotelSearch } from '../hooks/useHotelSearch';
import HotelForm from './HotelForm';
import HotelDetails from './HotelDetails';
import './HotelSearch.css';

const HotelSearch = ({ onShowSavedHotels }) => {
  const {
    hotelName,
    setHotelName,
    loading,
    hotelData,
    saving,
    error,
    searchHotel,
    saveHotel,
    clearError
  } = useHotelSearch();

  return (
    <div className="hotel-search-container">
      <HotelForm
        hotelName={hotelName}
        setHotelName={setHotelName}
        onSearch={searchHotel}
        loading={loading}
        error={error}
        onClearError={clearError}
      />
      
      <HotelDetails
        hotelData={hotelData}
        onSave={saveHotel}
        saving={saving}
        onShowSavedHotels={onShowSavedHotels}
      />
    </div>
  );
};

export default HotelSearch;