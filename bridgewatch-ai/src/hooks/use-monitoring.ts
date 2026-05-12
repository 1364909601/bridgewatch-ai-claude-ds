import { useQuery } from "@tanstack/react-query";
import { getMonitoringData } from "../lib/api";

export function useMonitoringData(
  objectId: string,
  dataTypes?: string,
  options?: { limit?: number }
) {
  return useQuery({
    queryKey: ["monitoring", objectId, dataTypes, options?.limit],
    queryFn: () =>
      getMonitoringData({
        object_id: objectId,
        data_types: dataTypes,
        limit: options?.limit,
      }),
    enabled: !!objectId,
  });
}
