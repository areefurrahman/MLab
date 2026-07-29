// frontend/src/hooks/useExperimentPolling.js

import { useQuery } from "@tanstack/react-query";
import { experimentsApi } from "../api/experimentsApi";

const TERMINAL_STATES = ["completed", "failed"];

export function useExperimentPolling(experimentId) {
  return useQuery({
    queryKey: ["experiment", experimentId],
    queryFn: () => experimentsApi.get(experimentId),
    enabled: !!experimentId,

    // Re-run this function after every fetch — return a number (ms) to keep
    // polling, or `false` to stop. This is React Query's built-in polling.
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (TERMINAL_STATES.includes(status)) {
        return false; // stop polling — we're done
      }
      return 1000; // poll every 1 second while pending/running
    },
  });
}