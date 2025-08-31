import React, { useState } from 'react';
import './App.css';
import HotelSearch from './components/HotelSearch';
import HotelList from './components/HotelList';

function App() {
  const [currentView, setCurrentView] = useState('search');

  const showHotelList = () => {
    setCurrentView('list');
  };

  const showHotelSearch = () => {
    setCurrentView('search');
  };

  return (
    <div className="App">
      <nav className="app-nav">
        <button 
          className={`nav-button ${currentView === 'search' ? 'active' : ''}`}
          onClick={showHotelSearch}
        >
          Buscar Hoteles
        </button>
        <button 
          className={`nav-button ${currentView === 'list' ? 'active' : ''}`}
          onClick={showHotelList}
        >
          Hoteles Guardados
        </button>
      </nav>

      {currentView === 'search' ? (
        <HotelSearch onShowSavedHotels={showHotelList} />
      ) : (
        <HotelList onBackToSearch={showHotelSearch} />
      )}
    </div>
  );
}

export default App;
