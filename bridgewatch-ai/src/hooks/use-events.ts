import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getEvents, getEventDetail, reviewEvent } from "../lib/api";
import type { EventQueryParams } from "../lib/api";

export function useEventList(params?: EventQueryParams) {
  return useQuery({
    queryKey: ["events", "list", params],
    queryFn: () => getEvents(params),
  });
}

export function useEventDetail(eventId: string | null) {
  return useQuery({
    queryKey: ["events", "detail", eventId],
    queryFn: () => getEventDetail(eventId!),
    enabled: !!eventId,
  });
}

export function useReviewEvent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      eventId,
      review_status,
      review_remark,
    }: {
      eventId: string;
      review_status: string;
      review_remark?: string;
    }) => reviewEvent(eventId, { review_status, review_remark }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events"] });
    },
  });
}
