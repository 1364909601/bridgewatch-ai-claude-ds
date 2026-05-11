import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getAlerts, getUnreadAlertCount, acknowledgeAlert, batchAcknowledgeAlerts } from "../lib/api";
import type { AlertItem } from "../lib/api";

export function useUnreadAlertCount() {
  return useQuery({
    queryKey: ["alerts", "unread-count"],
    queryFn: () => getUnreadAlertCount(),
    refetchInterval: 30_000, // poll every 30s
  });
}

export function useAlerts(params?: {
  page_no?: number;
  page_size?: number;
  status?: string;
  severity?: string;
}) {
  return useQuery({
    queryKey: ["alerts", "list", params],
    queryFn: () => getAlerts(params),
  });
}

export function useAcknowledgeAlert() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (alertId: string) => acknowledgeAlert(alertId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["alerts"] });
    },
  });
}

export function useBatchAcknowledgeAlerts() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (alertIds: string[]) => batchAcknowledgeAlerts(alertIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["alerts"] });
    },
  });
}
