import axios from "axios";
import { ACCESS_TOKEN } from "../utils/constant";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
  withCredentials: true, // Needed if using cookies (not strictly needed for token headers)
});

// Add token to headers
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
