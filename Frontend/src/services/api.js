import axios from 'axios';

// API base configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch {
        // Refresh token failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API methods
export const authAPI = {
  login: async (credentials) => {
    const response = await api.post('/token/', credentials);
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/users/register/', userData);
    return response.data;
  },

  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await api.post('/users/logout/', { refresh_token: refreshToken });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  verifyCode: async (data) => {
    const response = await api.post('/users/verify-code/', data);
    return response.data;
  },

  sendVerificationCode: async (data) => {
    const response = await api.post('/users/send-verification-code/', data);
    return response.data;
  },

  changePassword: async (data) => {
    const response = await api.post('/users/change-password/', data);
    return response.data;
  },
};

// User API methods
export const userAPI = {
  getProfile: async () => {
    const response = await api.get('/users/profile/');
    return response.data;
  },

  updateProfile: async (userData) => {
    const response = await api.put('/users/profile/', userData);
    return response.data;
  },

  getPassport: async () => {
    const response = await api.get('/users/passport/');
    return response.data;
  },

  updatePassport: async (passportData) => {
    const response = await api.put('/users/passport/', passportData);
    return response.data;
  },

  getDocuments: async () => {
    const response = await api.get('/users/documents/');
    return response.data;
  },

  uploadDocument: async (documentData) => {
    const response = await api.post('/users/documents/', documentData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  deleteDocument: async (documentId) => {
    const response = await api.delete(`/users/documents/${documentId}/`);
    return response.data;
  },
};

// Orders API methods
export const ordersAPI = {
  getOrders: async () => {
    const response = await api.get('/orders/');
    return response.data;
  },

  getOrder: async (orderId) => {
    const response = await api.get(`/orders/${orderId}/`);
    return response.data;
  },

  createOrder: async (orderData) => {
    const response = await api.post('/orders/', orderData);
    return response.data;
  },

  updateOrder: async (orderId, orderData) => {
    const response = await api.put(`/orders/${orderId}/`, orderData);
    return response.data;
  },

  deleteOrder: async (orderId) => {
    const response = await api.delete(`/orders/${orderId}/`);
    return response.data;
  },
};

// Declarations API methods
export const declarationsAPI = {
  getDeclarations: async () => {
    const response = await api.get('/declarations/');
    return response.data;
  },

  getDeclaration: async (declarationId) => {
    const response = await api.get(`/declarations/${declarationId}/`);
    return response.data;
  },

  createDeclaration: async (declarationData) => {
    const response = await api.post('/declarations/', declarationData);
    return response.data;
  },

  updateDeclaration: async (declarationId, declarationData) => {
    const response = await api.put(`/declarations/${declarationId}/`, declarationData);
    return response.data;
  },

  deleteDeclaration: async (declarationId) => {
    const response = await api.delete(`/declarations/${declarationId}/`);
    return response.data;
  },

  submitDeclaration: async (declarationId) => {
    const response = await api.post(`/declarations/${declarationId}/submit/`);
    return response.data;
  },

  generatePDF: async (declarationId) => {
    const response = await api.get(`/declarations/${declarationId}/generate-pdf/`, {
      responseType: 'blob',
    });
    return response.data;
  },

  getDeclarationStatistics: async () => {
    const response = await api.get('/declarations/statistics/');
    return response.data;
  },
};

// News API methods
export const newsAPI = {
  getNews: async () => {
    const response = await api.get('/news/');
    return response.data;
  },

  getNewsItem: async (newsId) => {
    const response = await api.get(`/news/${newsId}/`);
    return response.data;
  },
};

// Support API methods
export const supportAPI = {
  getTickets: async () => {
    const response = await api.get('/support/tickets/');
    return response.data;
  },

  getTicket: async (ticketId) => {
    const response = await api.get(`/support/tickets/${ticketId}/`);
    return response.data;
  },

  createTicket: async (ticketData) => {
    const response = await api.post('/support/tickets/', ticketData);
    return response.data;
  },

  updateTicket: async (ticketId, ticketData) => {
    const response = await api.put(`/support/tickets/${ticketId}/`, ticketData);
    return response.data;
  },

  deleteTicket: async (ticketId) => {
    const response = await api.delete(`/support/tickets/${ticketId}/`);
    return response.data;
  },

  getTicketReplies: async (ticketId) => {
    const response = await api.get(`/support/tickets/${ticketId}/replies/`);
    return response.data;
  },

  createTicketReply: async (ticketId, replyData) => {
    const response = await api.post(`/support/tickets/${ticketId}/replies/`, replyData);
    return response.data;
  },
};

export default api; 