import Link from "next/link";

import { SignOutButton } from "@/components/sign-out-button";

type AppShellProps = {
  role: "admin" | "viewer";
  user: { email: string; displayName: string | null; photoUrl: string | null };
  children: React.ReactNode;
};

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/historical", label: "Historical" },
  { href: "/reports", label: "Reports" },
  { href: "/insights", label: "AI Insights" },
];

const ADMIN_NAV_ITEMS = [
  { href: "/settings/uploads", label: "Uploads" },
  { href: "/settings", label: "Settings" },
];

export function AppShell({ role, user, children }: AppShellProps) {
  return (
    <div className="flex min-h-screen">
      <aside className="flex w-56 flex-col border-r border-border p-4">
        <div className="mb-6 text-sm font-semibold">Aspora Dashboard</div>
        <nav className="flex flex-1 flex-col gap-1">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
            >
              {item.label}
            </Link>
          ))}
          {role === "admin" && (
            <>
              <div className="mt-4 px-3 text-xs font-medium uppercase text-muted-foreground/70">
                Admin
              </div>
              {ADMIN_NAV_ITEMS.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
                >
                  {item.label}
                </Link>
              ))}
            </>
          )}
        </nav>
        <div className="mt-4 border-t border-border pt-4">
          <div className="truncate text-xs text-muted-foreground">{user.email}</div>
          <SignOutButton />
        </div>
      </aside>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
