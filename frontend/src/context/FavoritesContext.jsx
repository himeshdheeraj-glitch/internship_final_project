import React, { createContext, useState, useEffect, useContext } from 'react';
import { useAuth } from './AuthContext';
import { favoritesService } from '../services/api';

const FavoritesContext = createContext(null);

export const FavoritesProvider = ({ children }) => {
  const [favorites, setFavorites] = useState([]);
  const { isAuthenticated } = useAuth();

  // Load favorites when authentication state changes
  useEffect(() => {
    const loadFavorites = async () => {
      if (isAuthenticated) {
        try {
          const response = await favoritesService.getFavorites();
          // API returns response.data.items which contains list of favorites
          // Each favorite might have property_id or property details
          const items = response.data?.items || [];
          const favoriteIds = items.map((fav) => fav.property_id || fav.id);
          setFavorites(favoriteIds);
        } catch (error) {
          console.error('Failed to load favorites from server:', error);
          loadLocalFavorites();
        }
      } else {
        loadLocalFavorites();
      }
    };

    loadFavorites();
  }, [isAuthenticated]);

  const loadLocalFavorites = () => {
    const local = localStorage.getItem('favorites');
    if (local) {
      try {
        setFavorites(JSON.parse(local));
      } catch (e) {
        setFavorites([]);
      }
    } else {
      setFavorites([]);
    }
  };

  const toggleFavorite = async (propertyId) => {
    const isFav = favorites.includes(propertyId);
    let updated;
    
    if (isFav) {
      updated = favorites.filter((id) => id !== propertyId);
    } else {
      updated = [...favorites, propertyId];
    }
    
    // Update local state first for instant response
    setFavorites(updated);
    
    if (isAuthenticated) {
      try {
        if (isFav) {
          await favoritesService.removeFavorite(propertyId);
        } else {
          await favoritesService.addFavorite(propertyId);
        }
      } catch (error) {
        console.error('Failed to sync favorite with server:', error);
        // Revert on error
        setFavorites(favorites);
      }
    } else {
      localStorage.setItem('favorites', JSON.stringify(updated));
    }
  };

  const isFavorite = (propertyId) => favorites.includes(propertyId);

  return (
    <FavoritesContext.Provider value={{ favorites, toggleFavorite, isFavorite }}>
      {children}
    </FavoritesContext.Provider>
  );
};

export const useFavorites = () => useContext(FavoritesContext);
export default FavoritesContext;
