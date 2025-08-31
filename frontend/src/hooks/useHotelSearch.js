import { useState } from 'react';
import { apiUrl } from '../config';

export const useHotelSearch = () => {
  const [hotelName, setHotelName] = useState('');
  const [loading, setLoading] = useState(false);
  const [hotelData, setHotelData] = useState(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const searchHotel = async () => {
    if (!hotelName.trim()) {
      setError('Por favor ingresa el nombre del hotel');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${apiUrl}/api/v1/hotels/scrape/?name=${encodeURIComponent(hotelName)}`);
      const result = await response.json();
      
      if (result.ok) {
        setHotelData(result.data);
      } else {
        setError(result.msg || 'Error searching hotel');
        setHotelData(null);
      }
    } catch (error) {
      setError(`Error searching hotel: ${error.message}`);
      setHotelData(null);
    }
    
    setLoading(false);
  };

  const saveHotel = async () => {
    if (!hotelData) return;

    setSaving(true);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/api/v1/hotels/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(hotelData),
      });

      const result = await response.json();
      
      if (result.ok) {
        alert(result.msg || `Hotel saved with ID: ${result.data.hotel_id}`);
        setHotelData(null);
        setHotelName('');
        return result;
      } else {
        setError(result.msg || 'Error saving hotel');
      }
      
    } catch (error) {
      setError(`Error saving hotel: ${error.message}`);
    }

    setSaving(false);
  };

  const clearError = () => {
    setError(null);
  };

  return {
    hotelName,
    setHotelName,
    loading,
    hotelData,
    saving,
    error,
    searchHotel,
    saveHotel,
    clearError
  };
};