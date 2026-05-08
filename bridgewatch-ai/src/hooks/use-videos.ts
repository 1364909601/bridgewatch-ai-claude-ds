import { useQuery } from "@tanstack/react-query";
import { getVideos, getVideoEvents, getVideoPlayUrl } from "../lib/api";

export function useVideoList(params?: { page_no?: number; page_size?: number; object_id?: string; scene_type?: string }) {
  return useQuery({
    queryKey: ["videos", "list", params],
    queryFn: () => getVideos(params),
  });
}

export function useVideoEvents(videoId: string | null) {
  return useQuery({
    queryKey: ["videos", "events", videoId],
    queryFn: () => getVideoEvents(videoId!),
    enabled: !!videoId,
  });
}

export function useVideoPlayUrl(videoId: string | null) {
  return useQuery({
    queryKey: ["videos", "play-url", videoId],
    queryFn: () => getVideoPlayUrl(videoId!),
    enabled: !!videoId,
  });
}
