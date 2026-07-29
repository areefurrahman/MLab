// frontend/src/api/inferenceApi.js

import axiosInstance from "./axiosInstance";

export const inferenceApi = {
  listTasks: async () => {
    const res = await axiosInstance.get("/inference/tasks");
    return res.data;
  },
  run: async (taskName, inputData) => {
    const res = await axiosInstance.post("/inference/run", {
      task_name: taskName,
      input_data: inputData,
    });
    return res.data;
  },
  get: async (id) => {
    const res = await axiosInstance.get(`/inference/${id}`);
    return res.data;
  },

  runVoiceQA: async (audioFile) => {
  const formData = new FormData();
  formData.append("audio", audioFile);
  const res = await axiosInstance.post("/inference/run-voice-qa", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
},
};