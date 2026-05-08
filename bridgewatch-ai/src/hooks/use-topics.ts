import { useQuery } from "@tanstack/react-query";
import { getBridgeSummary, getShipCollisionFusion, getObjects, getDicts } from "../lib/api";

export function useBridgeSummary(object_id?: string) {
  return useQuery({
    queryKey: ["topics", "bridge-summary", object_id],
    queryFn: () => getBridgeSummary(object_id),
  });
}

export function useShipCollisionFusion(params: { object_id: string; start_time?: string; end_time?: string }) {
  return useQuery({
    queryKey: ["topics", "ship-collision", params],
    queryFn: () => getShipCollisionFusion(params),
    enabled: !!params.object_id,
  });
}

export function useObjectList(params?: { object_type?: string; status?: string }) {
  return useQuery({
    queryKey: ["objects", params],
    queryFn: () => getObjects(params),
  });
}

export function useDicts(dictType: string | null) {
  return useQuery({
    queryKey: ["dicts", dictType],
    queryFn: () => getDicts(dictType!),
    enabled: !!dictType,
  });
}
