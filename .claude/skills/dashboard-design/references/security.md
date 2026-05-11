# Security Defaults

Read this in Phase 2. Phase 1 uses mock data, so most of this doesn't apply yet — but the Zod schemas you wrote in Phase 1 become the validation layer in Phase 2, so don't wait to add them.

## Core principle

**Secure by default, least privilege, validated at every boundary.** The UI is not a security layer — server-side enforcement is.

## Non-negotiables

- **RBAC on the server.** Permissions checked in Server Actions / route handlers / RLS policies. Never rely on "the UI hides the button" — API calls can be made directly.
- **Zod validates every input.** The same schema that powered the form in Phase 1 now also runs on the server before any DB write. Parse, don't just validate — typed output is safer than a boolean.
- **Row Level Security** on every Supabase table. Even read-only tables. RLS off → delete the table and start over.
- **Secrets never touch the client.** `NEXT_PUBLIC_*` for anything the browser can see; everything else stays server-side. Service role keys in particular must only exist in server modules.
- **Safe error handling.** Surface user-friendly messages; log the stack trace server-side. Never send a raw DB error to the client — it leaks schema.

## OWASP Top 10 checklist

Quick pass before shipping:

- [ ] Broken access control → RBAC enforced server-side on every mutation
- [ ] Cryptographic failures → TLS everywhere, no plaintext secrets, hashed passwords (your auth provider handles this if you picked Clerk/Auth.js)
- [ ] Injection → Drizzle parameterizes; never build queries with string concatenation
- [ ] Insecure design → threat-model destructive flows before shipping (who can delete what, who can export what)
- [ ] Security misconfiguration → no debug endpoints in prod; error pages don't leak stack traces
- [ ] Vulnerable components → `npm audit` clean before deploy
- [ ] Auth failures → session timeout sensible, rate-limit login
- [ ] Data integrity → CSRF on forms (Server Actions handle this), verify webhooks
- [ ] Logging failures → audit log for create/update/delete on sensitive entities
- [ ] SSRF → validate URLs before fetching; no user-supplied URLs hitting internal services

## Rate limiting

Add Upstash rate limiting on:

- Auth endpoints (login, signup, password reset)
- Any AI endpoint (token costs add up fast)
- Mutations on public-ish routes
- Search / list endpoints if the data is sensitive

Default to "per user + per IP". Return `429` with a `Retry-After` header.

## Audit logging

For destructive or sensitive actions (delete, export, permission change, billing change), write an audit log entry: actor, action, target, timestamp, IP. A small `audit_logs` table on Supabase is enough. Query it when something goes wrong.
