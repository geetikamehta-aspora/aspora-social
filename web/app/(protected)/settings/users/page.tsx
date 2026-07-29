"use client";

import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/lib/auth/use-auth";
import { useCreateInvitation, useInvitations, useRevokeInvitation } from "@/lib/queries/invitations";
import { useUpdateUserRole, useUsers } from "@/lib/queries/users";

export default function UsersSettingsPage() {
  const { user } = useAuth();
  const { data: users, isLoading } = useUsers();
  const updateRole = useUpdateUserRole();

  const { data: invitations } = useInvitations();
  const createInvitation = useCreateInvitation();
  const revokeInvitation = useRevokeInvitation();

  const [email, setEmail] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [role, setRole] = useState<"admin" | "viewer">("viewer");

  async function handleInvite(e: React.FormEvent) {
    e.preventDefault();
    if (!user || !email.trim()) return;
    try {
      await createInvitation.mutateAsync({ email, displayName, role, invitedBy: user.uid });
      toast.success(`${email} can now log in as ${role} — role applies on their first sign-in.`);
      setEmail("");
      setDisplayName("");
      setRole("viewer");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to add user");
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-lg font-semibold">Users</h1>

      <Card>
        <CardHeader>
          <CardTitle>Add user</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleInvite} className="grid grid-cols-2 gap-3">
            <input
              type="email"
              required
              placeholder="email@aspora.com"
              className="h-9 rounded-lg border border-border bg-background px-3 text-sm"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="text"
              placeholder="Name (optional)"
              className="h-9 rounded-lg border border-border bg-background px-3 text-sm"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
            />
            <select
              className="h-9 rounded-lg border border-border bg-background px-3 text-sm"
              value={role}
              onChange={(e) => setRole(e.target.value as "admin" | "viewer")}
            >
              <option value="viewer">Viewer</option>
              <option value="admin">Admin</option>
            </select>
            <Button type="submit" disabled={createInvitation.isPending}>
              {createInvitation.isPending ? "Adding..." : "Add"}
            </Button>
          </form>
          <p className="mt-2 text-xs text-muted-foreground">
            They&apos;ll get this role automatically the first time they sign in with Google — no
            action needed from them beforehand.
          </p>
        </CardContent>
      </Card>

      {invitations && invitations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Pending invitations</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            {invitations.map((inv) => (
              <div key={inv.id} className="flex items-center justify-between text-sm">
                <span>
                  {inv.email} {inv.display_name && `(${inv.display_name})`} — {inv.role}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => revokeInvitation.mutate(inv.id)}
                >
                  Revoke
                </Button>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Active users</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading && <p className="p-4 text-sm text-muted-foreground">Loading...</p>}
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-left text-muted-foreground">
                <th className="p-3">Email</th>
                <th className="p-3">Name</th>
                <th className="p-3">Role</th>
              </tr>
            </thead>
            <tbody>
              {users?.map((u) => (
                <tr key={u.id} className="border-b border-border last:border-0">
                  <td className="p-3">{u.email}</td>
                  <td className="p-3">{u.display_name ?? "—"}</td>
                  <td className="p-3">
                    <select
                      className="h-8 rounded-md border border-border bg-background px-2 text-sm"
                      value={u.role}
                      onChange={(e) => {
                        const newRole = e.target.value as "admin" | "viewer";
                        updateRole.mutate(
                          { id: u.id, role: newRole },
                          {
                            onError: () => toast.error("Failed to update role"),
                            onSuccess: () => toast.success(`${u.email} is now ${newRole}`),
                          }
                        );
                      }}
                    >
                      <option value="viewer">Viewer</option>
                      <option value="admin">Admin</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
