import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { supabase } from "@/lib/supabase/client";

export type Invitation = {
  id: string;
  email: string;
  display_name: string | null;
  role: "admin" | "viewer";
  created_at: string;
};

export function useInvitations() {
  return useQuery({
    queryKey: ["invitations"],
    queryFn: async (): Promise<Invitation[]> => {
      const { data, error } = await supabase
        .from("invited_users")
        .select("id, email, display_name, role, created_at")
        .order("created_at", { ascending: false });
      if (error) throw error;
      return data;
    },
  });
}

export function useCreateInvitation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (input: {
      email: string;
      displayName: string;
      role: "admin" | "viewer";
      invitedBy: string;
    }) => {
      const { error } = await supabase.from("invited_users").insert({
        email: input.email.trim().toLowerCase(),
        display_name: input.displayName.trim() || null,
        role: input.role,
        invited_by: input.invitedBy,
      });
      if (error) throw error;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["invitations"] }),
  });
}

export function useRevokeInvitation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase.from("invited_users").delete().eq("id", id);
      if (error) throw error;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["invitations"] }),
  });
}
