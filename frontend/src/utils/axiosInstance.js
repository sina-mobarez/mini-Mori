import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'accept': 'application/json',
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
