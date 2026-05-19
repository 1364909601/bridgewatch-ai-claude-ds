import { useQuery } from "@tanstack/react-query";
import { getAuditLogs } from "../lib/api";

export function useAuditLogs(params?: {
  page_no?: number;
  page_size?: number;
  log_type?: string;
  log_level?: string;
}) {
  return useQuery({
    queryKey: ["audit", params],
    queryFn: () => getAuditLogs(params),
  });
}
