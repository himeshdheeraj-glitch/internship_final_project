import React, { createContext, useContext, useState } from 'react';
import { authService } from '../services/api';
import { useAuth } from './AuthContext';
import { normalizeUser } from './authUtils';

const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
  const { setUser } = useAuth();
  const [updating, setUpdating] = useState(false);

  const updateProfile = async (data) => {
    setUpdating(true);
    try {
      const updatedUser = normalizeUser(await authService.updateProfile(data));
      setUser(updatedUser);
      return updatedUser;
    } catch (e) {
      throw e;
    } finally {
      setUpdating(false);
    }
  };

  return (
    <UserContext.Provider value={{ updateProfile, updating }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
