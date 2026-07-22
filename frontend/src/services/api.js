import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          const { access_token, refresh_token } = response.data.data;
          
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const propertyService = {
  getProperties: async (params = {}) => {
    const normalizedParams = { ...params };
    if (normalizedParams.limit !== undefined && normalizedParams.size === undefined) {
      normalizedParams.size = normalizedParams.limit;
      delete normalizedParams.limit;
    }
    if (normalizedParams.offset !== undefined && normalizedParams.page === undefined) {
      normalizedParams.page = Math.floor(normalizedParams.offset / (normalizedParams.size || 20)) + 1;
      delete normalizedParams.offset;
    }

    const res = await api.get('/properties', { params: normalizedParams });
    return res.data.data;
  },
  getProperty: async (id) => {
    const res = await api.get(`/properties/${id}`);
    return res.data.data;
  },
  createProperty: async (data) => {
    const res = await api.post('/properties', data);
    return res.data.data;
  },
  updateProperty: async (id, data) => {
    const res = await api.put(`/properties/${id}`, data);
    return res.data.data;
  },
  deleteProperty: async (id) => {
    const res = await api.delete(`/properties/${id}`);
    return res.data.data;
  },
  uploadImage: async (propertyId, file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post(`/properties/${propertyId}/images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percent);
        }
      }
    });
    return res.data.data;
  },
  setCoverImage: async (propertyId, imageId) => {
    const res = await api.post(`/properties/${propertyId}/images/${imageId}/set-cover`);
    return res.data.data;
  },
  deleteImage: async (imageId) => {
    const res = await api.delete(`/properties/images/${imageId}`);
    return res.data.data;
  },
  getPropertyTypes: async () => {
    const res = await api.get('/property-types');
    return res.data.data;
  },
  createPropertyType: async (data) => {
    const res = await api.post('/property-types', data);
    return res.data.data;
  },
  deletePropertyType: async (id) => {
    const res = await api.delete(`/property-types/${id}`);
    return res.data.data;
  }
};

export const locationsService = {
  getCountries: async () => {
    const res = await api.get('/locations/countries');
    return res.data.data;
  },
  createCountry: async (data) => {
    const res = await api.post('/locations/countries', data);
    return res.data.data;
  },
  getStates: async (countryId) => {
    const res = await api.get(`/locations/countries/${countryId}/states`);
    return res.data.data;
  },
  createState: async (data) => {
    const res = await api.post('/locations/states', data);
    return res.data.data;
  },
  getCities: async (stateId) => {
    const res = await api.get(`/locations/states/${stateId}/cities`);
    return res.data.data;
  },
  createCity: async (data) => {
    const res = await api.post('/locations/cities', data);
    return res.data.data;
  }
};

export const amenitiesService = {
  getAmenities: async () => {
    const res = await api.get('/amenities');
    return res.data.data;
  },
  createAmenity: async (data) => {
    const res = await api.post('/amenities', data);
    return res.data.data;
  }
};

export const favoritesService = {
  getFavorites: async (params) => {
    const res = await api.get('/favorites', { params });
    return res.data.data;
  },
  addFavorite: async (propertyId) => {
    const res = await api.post(`/favorites/${propertyId}`);
    return res.data.data;
  },
  removeFavorite: async (propertyId) => {
    const res = await api.delete(`/favorites/${propertyId}`);
    return res.data.data;
  }
};

export const authService = {
  login: async (credentials) => {
    const res = await api.post('/auth/login', credentials);
    return res.data.data;
  },
  register: async (data) => {
    const res = await api.post('/auth/register', data);
    return res.data.data;
  },
  logout: async () => {
    const res = await api.post('/auth/logout');
    return res.data.data;
  },
  getMe: async () => {
    const res = await api.get('/users/me');
    return res.data.data;
  },
  updateProfile: async (data) => {
    const res = await api.put('/users/me', data);
    return res.data.data;
  }
};

export const adminService = {
  getUsers: async (params) => {
    const res = await api.get('/admin/users', { params });
    return res.data.data;
  },
  updateUserRole: async (userId, roleName) => {
    const res = await api.put(`/admin/users/${userId}/role`, { role_name: roleName });
    return res.data.data;
  },
  deactivateUser: async (userId) => {
    const res = await api.post(`/admin/users/${userId}/deactivate`);
    return res.data.data;
  },
  deleteUser: async (userId) => {
    const res = await api.delete(`/admin/users/${userId}`);
    return res.data.data;
  },
  getAdminProperties: async (params = {}) => {
    const res = await api.get('/admin/properties', { params });
    return res.data.data;
  },
  updatePropertyStatus: async (propertyId, statusVal) => {
    const res = await api.put(`/admin/properties/${propertyId}/status`, null, {
      params: { status_val: statusVal }
    });
    return res.data.data;
  },
  getDashboardAnalytics: async () => {
    const res = await api.get('/admin/analytics/dashboard');
    return res.data.data;
  }
};

export const reviewsService = {
  getPropertyReviews: async (propertyId) => {
    const res = await api.get(`/reviews/property/${propertyId}`);
    return res.data.data;
  },
  createReview: async (data) => {
    const res = await api.post('/reviews', data);
    return res.data.data;
  },
  deleteReview: async (id) => {
    const res = await api.delete(`/reviews/${id}`);
    return res.data.data;
  }
};

export default api;
