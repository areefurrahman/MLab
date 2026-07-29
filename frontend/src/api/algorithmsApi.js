// frontend/src/api/algorithmsApi.js — add a combined fetch

import axiosInstance from "./axiosInstance";
import { inferenceApi } from "./inferenceApi";

export const algorithmsApi = {
  list: async () => {
    const res = await axiosInstance.get("/algorithms");
    return res.data;
  },

  listAllForLibrary: async () => {
    // Merge classical algorithms + inference tasks for the Library page
    const [algos, tasks] = await Promise.all([
      axiosInstance.get("/algorithms").then((r) => r.data),
      axiosInstance.get("/inference/tasks").then((r) => r.data),
    ]);

    // Normalize inference tasks to match algorithm card shape
    const normalizedTasks = tasks.map((t) => ({
      ...t,
      task_type: "inference",
      is_inference: true,
      link_to: `/infer/${t.name}`,  // inference tasks go to their own page
    }));

    return [...algos, ...normalizedTasks];
  },
};