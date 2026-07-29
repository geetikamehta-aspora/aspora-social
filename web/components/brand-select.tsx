"use client";

import { type Brand } from "@/lib/queries/brands";

export function BrandSelect({
  brands,
  value,
  onChange,
}: {
  brands: Brand[];
  value: string | undefined;
  onChange: (brandId: string) => void;
}) {
  return (
    <select
      className="h-9 rounded-lg border border-border bg-background px-3 text-sm"
      value={value ?? ""}
      onChange={(e) => onChange(e.target.value)}
    >
      {brands.map((brand) => (
        <option key={brand.id} value={brand.id}>
          {brand.name}
        </option>
      ))}
    </select>
  );
}
