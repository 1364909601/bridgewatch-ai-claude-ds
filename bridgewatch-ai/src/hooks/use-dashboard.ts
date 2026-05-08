import { useQuery } from "@tanstack/react-query";
import { getDashboardSummary, getDashboardTrend, getDashboardDistribution } from "../lib/api";

export function useDashboardSummary(params?: {
  start_time?: string;
  end_time?: string;
  object_type?: string;
  object_id?: string;
  scene_type?: string;
}) {
  return useQuery({
    queryKey: ["dashboard", "summary", params],
    queryFn: () => getDashboardSummary(params),
  });
}

export function useDashboardTrend(days: number = 7) {
  return useQuery({
    queryKey: ["dashboard", "trend", days],
    queryFn: () => getDashboardTrend(days),
  });
}

export function useDashboardDistribution() {
  return useQuery({
    queryKey: ["dashboard", "distribution"],
    queryFn: getDashboardDistribution,
  });
}
