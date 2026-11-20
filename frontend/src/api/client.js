import axios from 'axios';

// Get API base URL from environment variable (set at build time by Vite)
// Falls back to '/api' for development (proxied via Vite) or when served from same domain
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for cookies/JWT if using httpOnly cookies
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      // Only redirect if not already on login page (avoid redirect loops)
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth endpoints
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/me'),
};

// Product endpoints
export const productAPI = {
  list: (params) => api.get('/products', { params }),
  categories: () => api.get('/products/categories'),
  get: (id) => api.get(`/products/${id}`),
};

// Customer endpoints
export const customerAPI = {
  // Cart
  getCart: () => api.get('/customer/cart'),
  addToCart: (data) => api.post('/customer/cart', data),
  updateCart: (id, data) => api.patch(`/customer/cart/${id}`, data),
  removeFromCart: (id) => api.delete(`/customer/cart/${id}`),

  // Wishlist
  getWishlist: () => api.get('/customer/wishlist'),
  toggleWishlist: (data) => api.post('/customer/wishlist/toggle', data),

  // Addresses
  getAddresses: () => api.get('/customer/addresses'),
  createAddress: (data) => api.post('/customer/addresses', data),
  deleteAddress: (id) => api.delete(`/customer/addresses/${id}`),

  // Orders
  createOrder: (data) => api.post('/customer/orders', data),
  getOrders: () => api.get('/customer/orders'),
};

// Admin endpoints
export const adminAPI = {
  // Products
  listProducts: (params) => api.get('/admin/products', { params }),
  createProduct: (data) => api.post('/admin/products', data),
  updateProduct: (id, data) => api.put(`/admin/products/${id}`, data),
  adjustStock: (id, data) => api.patch(`/admin/products/${id}/stock`, data),
  deleteProduct: (id) => api.delete(`/admin/products/${id}`),

  // Orders
  listOrders: (params) => api.get('/admin/orders', { params }),
  updateOrderStatus: (id, data) => api.patch(`/admin/orders/${id}/status`, data),

  // Analytics
  getAnalytics: (params) => api.get('/admin/analytics', { params }),
};