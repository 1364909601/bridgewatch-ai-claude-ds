import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createUser, deleteUser, getUsers, updateUser } from "../lib/api";
import type { UserItem } from "../lib/api";

export function useUserList() {
  return useQuery({
    queryKey: ["users"],
    queryFn: () => getUsers(),
  });
}

export function useCreateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { username: string; password: string; display_name: string; role: string }) =>
      createUser(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  });
}

export function useUpdateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { user_id: string; updates: Partial<Pick<UserItem, "display_name" | "role" | "is_active"> & { password?: string }> }) =>
      updateUser(data.user_id, data.updates),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  });
}

export function useDeleteUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (userId: string) => deleteUser(userId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  });
}
