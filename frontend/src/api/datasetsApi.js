// frontend/src/api/datasetsApi.js

import axiosInstance from "./axiosInstance";

export const datasetsApi = {
  listBuiltin: async () => {
    const res = await axiosInstance.get("/datasets/builtin");
    return res.data;
  },
  listMine: async () => {
    const res = await axiosInstance.get("/datasets");
    return res.data;
  },
  upload: async (file, name) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", name);
    const res = await axiosInstance.post("/datasets/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  },
};