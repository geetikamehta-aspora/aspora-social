import { useQuery } from "@tanstack/react-query";

import { supabase } from "@/lib/supabase/client";

export type Brand = {
  id: string;
  name: string;
  slug: string;
};

export function useBrands() {
  return useQuery({
    queryKey: ["brands"],
    queryFn: async (): Promise<Brand[]> => {
      const { data, error } = await supabase
        .from("brands")
        .select("id, name, slug")
        .eq("is_active", true)
        .order("name");
      if (error) throw error;
      return data;
    },
  });
}
