import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { supabase } from "@/lib/supabase/client";

export type AppUser = {
  id: string;
  email: string;
  display_name: string | null;
  photo_url: string | null;
  role: "admin" | "viewer";
  is_active: boolean;
};

export function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: async (): Promise<AppUser[]> => {
      const { data, error } = await supabase
        .from("users")
        .select("id, email, display_name, photo_url, role, is_active")
        .order("email");
      if (error) throw error;
      return data;
    },
  });
}

export function useUpdateUserRole() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, role }: { id: string; role: "admin" | "viewer" }) => {
      // Enforced server-side too: only an admin's write actually changes the
      // role column (trg_enforce_user_role_immutable in sql/003_rls.sql).
      const { error } = await supabase.from("users").update({ role }).eq("id", id);
      if (error) throw error;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  });
}
