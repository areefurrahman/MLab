// frontend/src/api/experimentsApi.js

import axiosInstance from "./axiosInstance";

export const experimentsApi = {
  run: async (payload) => {
    const res = await axiosInstance.post("/experiments/run", payload);
    return res.data;
  },
  get: async (id) => {
    const res = await axiosInstance.get(`/experiments/${id}`);
    return res.data;
  },
  list: async () => {
    const res = await axiosInstance.get("/experiments");
    return res.data;
  },
};