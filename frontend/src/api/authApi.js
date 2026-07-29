// frontend/src/api/authApi.js

import axiosInstance from "./axiosInstance";

export const authApi = {
  register: async (data) => {
    const response = await axiosInstance.post("/auth/register", data);
    return response.data;
  },

  login: async (data) => {
    const response = await axiosInstance.post("/auth/login", data);
    return response.data;
  },

  getMe: async () => {
    const response = await axiosInstance.get("/auth/me");
    return response.data;
  },

  refresh: async () => {
    const response = await axiosInstance.post("/auth/refresh");
    return response.data;
  },
};