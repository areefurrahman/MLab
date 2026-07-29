// frontend/src/hooks/useComparisonPolling.js

import { useQuery } from "@tanstack/react-query";
import { comparisonsApi } from "../api/comparisonsApi";

const TERMINAL_STATES = ["completed", "failed"];

export function useComparisonPolling(groupId) {
  return useQuery({
    queryKey: ["comparison", groupId],
    queryFn: () => comparisonsApi.get(groupId),
    enabled: !!groupId,
    refetchInterval: (query) => {
      const experiments = query.state.data?.experiments;
      if (!experiments) return 1000;
      const allDone = experiments.every((e) => TERMINAL_STATES.includes(e.status));
      return allDone ? false : 1000;   // stop only when EVERY child experiment is done
    },
  });
}