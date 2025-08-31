import React from 'react';

const HotelForm = ({ hotelName, setHotelName, onSearch, loading, error, onClearError }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      onSearch();
    }
  };

  const handleInputChange = (e) => {
    setHotelName(e.target.value);
    if (error) {
      onClearError();
    }
  };

  return (
    <div className="search-container">
      <h1>Search your Hotel</h1>
      
      <div className="search-info">
        <p>
          <strong>Configuración de búsqueda:</strong> 2 adultos, sin niños | 
          Fechas: 28/12/2025 - 29/12/2025 (1 noche)
        </p>
      </div>
      
      <div className="search-form">
        <input
          type="text"
          value={hotelName}
          onChange={handleInputChange}
          placeholder="Hotel's name"
          className="search-input"
          onKeyPress={handleKeyPress}
        />
        <button
          onClick={onSearch}
          disabled={loading}
          className={`search-button ${loading ? 'loading' : ''}`}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  );
};

export default HotelForm;