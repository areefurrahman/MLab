// frontend/src/hooks/useInferencePolling.js

import { useQuery } from "@tanstack/react-query";
import { inferenceApi } from "../api/inferenceApi";

const TERMINAL_STATES = ["completed", "failed"];

export function useInferencePolling(runId) {
  return useQuery({
    queryKey: ["inference", runId],
    queryFn: () => inferenceApi.get(runId),
    enabled: !!runId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return TERMINAL_STATES.includes(status) ? false : 1500;  // 1.5s — model runs take longer
    },
  });
}