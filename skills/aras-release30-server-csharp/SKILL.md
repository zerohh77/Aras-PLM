---
name: aras-release30-server-csharp
description: Use when writing, reviewing, optimizing, or debugging Aras Innovator Release 30 build 14.0.22.40048 server-side C#, including Server Methods, Server Events, IOM/AML, relationships, bulk changes, transactions, permissions, SQL boundaries, diagnostics, and runtime compatibility. Do not use as a generic C# guide.
---

# Aras Release 30 Server-side C#

## Scope

Implement server-side C# for **Aras Innovator Release 30, build 14.0.22.40048**. Platform facts remain owned by the sibling Core Skill; this Skill converts those facts into coding decisions.

Before coding, identify the Method kind, invocation action, `event_version`, context Item shape, expected response cardinality, caller Identity, transaction boundary, and hotfix state. Do not claim code is copy-ready while any of these materially changes behavior.

For a cold, uncertain, or high-risk question, inspect [COVERAGE.md](../references/COVERAGE.md) and then [SOURCES.md](../references/SOURCES.md); do not load them for routine coding.

## Runtime and compiler boundary

- Release 30 server components run on .NET 6.0.
- A custom DLL used by a Server Method must target .NET 6.0, reference the IOM assembly shipped with the exact deployment, be copied with symbols to `Server/bin`, and be registered in `Method-Config.xml` with its namespace/template and correct `line_number_offset`.
- The runtime version does not prove the Method compiler's C# language version. Follow syntax already accepted by the target Method template and compile-probe records, nullable-reference annotations, target-typed `new`, switch expressions, `using var`, or other newer syntax before adopting it.
- No general Release 30 contract was found for `async` or custom threads inside request-bound Server Methods. Do not detach work that depends on the request connection, Identity, transaction, or `this`; move long-running work to a documented background boundary.

## Server Method context and IOM

- Obtain the request-scoped connection with `Innovator inn = this.getInnovator()` when the Method contract supplies an Item context. Do not manufacture another session inside the Method.
- Treat `this` according to the invocation: action input, generic Method input, and Server Event request/response contexts are not interchangeable.
- `Item.apply()` sends the request DOM and returns a **new** response `Item`. Keep `request` and `response` variables separate. `loadAML()` instead replaces the current Item DOM.
- Check `isError()` first, then distinguish zero, one, and many results before accessing properties. Do not treat an empty result as a successful singleton.
- Build Items with `newItem`, `setID`, `setProperty`, `setAttribute`, and relationship APIs. Use raw AML only when nesting is clearer, construct it with XML APIs, and never interpolate untrusted values.
- Bound every query with explicit criteria, `select`, and paging or `maxRecords`; request `related_id(...)` properties only when needed.

## Actions, events, and results

- Choose `edit`, `update`, or `version` from the required lock and generation behavior; they are not synonyms. In Release 30, `update` requires a lock, `edit` performs lock/update/unlock, and a versionable first update after locking versions unless `version="0"`.
- `OnBefore*` validates or transforms request AML; an Error Item stops the action. `On*` replaces built-in behavior. `OnAfter*` observes response semantics and may still fail the Aras transaction.
- For event version 2, grouped `onAfterAdd`, `onAfterUpdate`, and `onAfterVersion` execute once for the request group with the result collection as context. Test `where`/`idList` and multi-ID requests; do not assume per-item invocation.
- Return the Item-shaped contract expected by the caller. Use `inn.newResult` for a documented scalar/result contract and `inn.newError` for safe failures. Do not force every successful Server Event to return a replacement Item.

## Relationships and versioning

- Keep source Item, Relationship Item, and related Item distinct. Store quantity, sequence, role, and other edge data on the Relationship Item.
- Use relationship APIs to attach a clean Relationship Item and related Item; do not mutate a related Item when the intent is to change the relationship row.
- Source versioning or cloning can clone relationship rows. Which related generation remains linked depends on RelationshipType behavior and lifecycle-state behavior; inspect both before implementing copy/version logic.

## Bulk operations and performance

1. Dry-run the exact IDs, count, and old values.
2. Use explicit-ID Item actions in bounded batches; do not use broad `where` writes.
3. Preserve events and permissions. Do not use `serverEvents="0"` as performance tuning; required events and edit lock events may still run.
4. Record a checkpoint, correlation ID, result count, and safe error per batch; make retry/resume idempotent.
5. Post-validate state and retain a rollback or compensation path.

Optimize only after measuring result count, selected properties, payload size, relationship depth, Method/Event duration, SQL blocking, and external-call duration. Prefer fewer bounded server requests over unbounded AML or recycled UI-context Items.

## Transactions, permissions, and SQL

- Let Aras own its database transaction; do not issue manual commit or rollback against the Innovator connection.
- A failed `OnAfter*` can roll back Aras data, not an email, HTTP call, queue publish, or external database write. Persist an outbox Item in the Aras transaction and process it with idempotency, bounded retry, dead-lettering, and reconciliation.
- Elevate only after ordinary permissions are proven insufficient. Use a dedicated least-privilege Identity, validate inputs first, narrow the scope, restore in `finally`, audit the action, and test cleanup. The exact Release 30 elevation signature remains runtime-sensitive; verify it rather than copying old `GrantIdentity`/`RevokeIdentity` snippets.
- Reject `applySQL`, stored procedures, and ad-hoc SQL for business writes. Read-only diagnostics require a DBA-controlled, least-privilege path and still do not enforce Aras permissions.

## Error handling and diagnostics

- Return a concise domain error plus correlation ID. Keep stack traces, paths, SQL, credentials, and sensitive AML in a protected, configured log sink.
- Do not assume `System.Diagnostics.Trace` is persisted. Verify sink, ACL, rotation, retention, and redaction.
- Diagnose from the failing hop and smallest request: capture build/hotfix, Method/event/action, `event_version`, caller Identity, target IDs, lock/generation, safe request shape, duration, and server logs.
- After a fix, add permitted/denied, zero/one/many, malformed, retry, concurrent-lock, and rollback tests as applicable.

## Dangerous assumptions

- Do not assume .NET 6 means every modern C# syntax feature is accepted by the Method compiler.
- Do not assume an Error Item, empty collection, and singleton have the same response shape.
- Do not assume `OnAfter` makes remote side effects transactional or exactly-once.
- Do not assume disabling events bypasses required or lock events.
- Do not assume a relationship grid row and its related Item are the same object.
- Do not assume elevated or direct-SQL code preserves the permission, event, lifecycle, history, or audit model.
