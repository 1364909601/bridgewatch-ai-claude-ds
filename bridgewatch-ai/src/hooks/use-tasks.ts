import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getInferenceTasks, createInferenceTask } from "../lib/api";

export function useInferenceTaskList(params?: { page_no?: number; page_size?: number; task_status?: string; video_id?: string }) {
  return useQuery({
    queryKey: ["tasks", "inference", params],
    queryFn: () => getInferenceTasks(params),
  });
}

export function useCreateInferenceTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (body: { video_id: string; model_id: string; task_name?: string }) =>
      createInferenceTask(body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
}
