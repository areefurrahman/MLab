// frontend/src/api/comparisonsApi.js

import axiosInstance from "./axiosInstance";

export const comparisonsApi = {
  run: async (payload) => {
    const res = await axiosInstance.post("/comparisons/run", payload);
    return res.data;
  },
  get: async (id) => {
    const res = await axiosInstance.get(`/comparisons/${id}`);
    return res.data;
  },
};