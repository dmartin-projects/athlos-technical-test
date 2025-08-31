import { useState, useEffect } from 'react';
import { apiUrl } from '../config';

export const useHotelList = () => {
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedHotel, setSelectedHotel] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [deleting, setDeleting] = useState(null);

  const fetchHotels = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${apiUrl}/api/v1/hotels/`);
      const result = await response.json();
      
      if (result.ok) {
        setHotels(result.data);
      } else {
        setError(result.msg || 'Error loading hotels');
      }
    } catch (error) {
      setError(`Error loading hotels: ${error.message}`);
    }
    
    setLoading(false);
  };

  const fetchHotelDetail = async (hotelId) => {
    setLoadingDetail(true);
    setError(null);
    
    try {
      const response = await fetch(`${apiUrl}/api/v1/hotels/${hotelId}/`);
      const result = await response.json();
      
      if (result.ok) {
        setSelectedHotel(result.data);
      } else {
        setError(result.msg || 'Error loading hotel information ');
        setSelectedHotel(null);
      }
    } catch (error) {
      setError(`Error loading hotel information: ${error.message}`);
      setSelectedHotel(null);
    }
    
    setLoadingDetail(false);
  };

  const deleteHotel = async (hotelId) => {
    if (!window.confirm('¿Are your sure deleting this Hotel?')) {
      return;
    }

    setDeleting(hotelId);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/api/v1/hotels/${hotelId}/`, {
        method: 'DELETE',
      });

      const result = await response.json();
      
      if (result.ok) {
        setHotels(hotels.filter(hotel => hotel.id !== hotelId));
        
        if (selectedHotel && selectedHotel.id === hotelId) {
          setSelectedHotel(null);
        }
      } else {
        setError(result.msg || 'Error deleting hotel');
      }

    } catch (error) {
      setError(`Error deleting hotel: ${error.message}`);
    }

    setDeleting(null);
  };

  const clearError = () => {
    setError(null);
  };

  const clearSelectedHotel = () => {
    setSelectedHotel(null);
  };

  useEffect(() => {
    fetchHotels();
  }, []);

  return {
    hotels,
    loading,
    error,
    selectedHotel,
    loadingDetail,
    deleting,
    fetchHotels,
    fetchHotelDetail,
    deleteHotel,
    clearError,
    clearSelectedHotel
  };
};