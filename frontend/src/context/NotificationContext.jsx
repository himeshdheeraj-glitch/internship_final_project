import React, { createContext, useContext } from 'react';
import toast, { Toaster } from 'react-hot-toast';

const NotificationContext = createContext(null);

export const NotificationProvider = ({ children }) => {
  const showSuccess = (msg) => toast.success(msg, {
    style: {
      borderRadius: '16px',
      background: '#ffffff',
      color: '#0f172a',
      border: '1px solid #e2e8f0',
      fontSize: '14px',
      fontWeight: '600'
    }
  });
  
  const showError = (msg) => toast.error(msg, {
    style: {
      borderRadius: '16px',
      background: '#ffffff',
      color: '#be123c',
      border: '1px solid #fecdd3',
      fontSize: '14px',
      fontWeight: '600'
    }
  });

  return (
    <NotificationContext.Provider value={{ showSuccess, showError }}>
      <Toaster position="top-right" reverseOrder={false} />
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotifications = () => useContext(NotificationContext);
