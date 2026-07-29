// frontend/src/api/historyApi.js

import axiosInstance from "./axiosInstance";

export const historyApi = {
  list: async ({ type, status } = {}) => {
    const params = {};
    if (type) params.type = type;
    if (status) params.status = status;
    const res = await axiosInstance.get("/history", { params });
    return res.data;
  },

  getExperiment: async (id) => {
    const res = await axiosInstance.get(`/history/experiment/${id}`);
    return res.data;
  },

  getComparison: async (id) => {
    const res = await axiosInstance.get(`/history/comparison/${id}`);
    return res.data;
  },

  getInference: async (id) => {
    const res = await axiosInstance.get(`/history/inference/${id}`);
    return res.data;
  },
};