---
name: aras-release30-webapi-csharp
description: Use when designing, implementing, reviewing, migrating, or debugging an external C# Web API that integrates with Aras Innovator Release 30 build 14.0.22.40048 through IOM/AML, Vault, SQL read models, or external services. Covers HTTP-to-Aras boundaries, connection lifetime, identity, errors, bulk work, async, files, configuration, and diagnostics. Do not use for in-platform Server Methods or generic ASP.NET guidance.
---

# Aras Release 30 Web API C#

## Scope and evidence gate

Build an **external or independently hosted C# Web API** that integrates with Aras Innovator Release 30, build `14.0.22.40048`. In-platform Server Methods and Events belong to `aras-release30-server-csharp`; platform semantics belong to `aras-release30-core`.

Before changing code, confirm the Web API target framework/hosting model, exact deployed IOM assembly, Innovator build and hotfix, API authentication, Aras identity model, connection wrapper, response contract, timeout boundary, and test surface. The Release 30 server's .NET 6 runtime does not prove that an external application's target framework or arbitrary IOM binary is compatible.

For cold, uncertain, or high-risk questions, inspect [COVERAGE.md](../references/COVERAGE.md) and then [SOURCES.md](../references/SOURCES.md). For task-specific names and behavior, search the live application source. This Skill deliberately stores no endpoint, DTO, controller, service, or business-object inventory.

## API and integration boundaries

Trace the whole path before implementing or diagnosing:

```text
HTTP binding and validation
  -> application/service operation
  -> Aras/SQL/Vault/external adapter
  -> Error Item or exception classification
  -> real HTTP status plus sanitized response
```

- Keep routing, transport validation, upload/download framing, cancellation acquisition, and HTTP response construction at the API boundary.
- Keep Aras operations, business validation, batching, and external orchestration in an application/service boundary that can be tested without an HTTP host.
- Keep IOM login/logout, SQL access, Vault streaming, and outbound HTTP behind explicit adapters. Do not open ad hoc sessions throughout controllers and services.
- The reference application contains both delegated and controller-heavy flows; do not present either local shape as universal. Follow a proven adjacent pattern only after tracing its error, identity, and disposal behavior.
- Use dependency injection or the application's existing composition boundary for lifetimes. Do not turn a process-wide service locator or singleton cache into a new convention merely because legacy code uses one.

## Runtime and IOM compatibility

- Treat the Web API runtime and Aras server runtime as separate compatibility decisions. Verify that the API target framework can load the **exact IOM assembly shipped for the target Innovator deployment** and run a login/query/logout smoke test.
- Do not reuse an IOM assembly from another checkout or release through an incidental file path. Record assembly provenance in deployment configuration and test it during an upgrade.
- Keep Release 30 action, result, relationship, permission, lifecycle, and File/Vault semantics in Core; use this Skill only to translate those semantics into HTTP-service behavior.

## Aras connection, session, and identity lifetime

- Prefer one explicitly owned connection/session per bounded API operation or background job, with deterministic login and logout/disposal in every outcome.
- Do not retain `Innovator`, connection, or mutable `Item` objects across unrelated requests, cache them as application data, or use one concurrently unless the exact IOM version's thread-safety and session-expiry contract has been proved.
- Cache neutral immutable values or serialized application data, not live IOM objects. Rehydrate a request with a current session and permission context.
- In the validated reference Web API implementation, a shared Aras connection abstraction owns the dominant configured-account session/reuse path, while a separate connection wrapper owns the disposable per-operation path. Reuse the abstraction already governing the target subsystem; do not bypass it with ad hoc `IomFactory` calls, introduce a third lifecycle, or redesign its reuse policy without focused runtime evidence. The observed shared path is not proof of thread safety.
- Caller-to-Aras identity mapping is endpoint-specific, not automatic: most inspected IOM paths execute with the configured technical account, while an explicit user-login path creates a user-scoped Aras session. No source-level HTTP-principal-to-Aras mapping or Identity impersonation layer was found. Trace the exact endpoint login path before treating Aras permissions as the HTTP caller's authorization.
- For a configured-account path, authorize the HTTP caller separately before invoking Aras. For an explicit user-login path, verify that the user mapping comes from an authenticated boundary; never trust a request username alone as proof of identity.
- If caller credentials or tokens are accepted, never log, cache, echo, or place them in URLs. If a service account is used, keep it least-privileged and enforce caller authorization before invoking it.

## IOM/AML, relationships, and errors

- Build requests with IOM Items and properties; use XML construction for genuinely hierarchical AML. Never concatenate request data into AML.
- Keep request and response Items separate. After every `apply`, `applyAML`, or Method invocation, check the Error Item before result count or property access; HTTP transport success does not prove Aras success.
- Distinguish error, zero, one, and many results. Preserve source Item, Relationship Item, and related Item as separate concepts.
- Translate failures once at the API boundary into stable categories: malformed/invalid input, unauthenticated or forbidden caller, missing/conflicting state, Aras domain failure, dependency timeout/unavailability, and unexpected server failure. Use real HTTP status codes from the API contract rather than returning HTTP 200 with an embedded failure code.
- Return a safe message and correlation ID. Keep stack traces, SQL, physical paths, credentials, full AML, and Aras error detail in protected logs only.
- Do not expose `getErrorString()` or exception text directly unless it has been classified as safe domain text. Preserve the original exception as the logged cause instead of replacing it with a message-only exception.

## Bulk work, SQL, and transaction boundaries

For imports or bulk changes:

1. Validate the entire input and resolve references before writing.
2. Bound input rows, query results, AML payload size, relationship depth, and duration.
3. Use parameterized, bounded read queries when a justified read model is required.
4. Build explicit IOM actions and submit a bounded Aras request; check the returned Error Item and expected result count.
5. Define all-or-nothing versus partial-success behavior, idempotency key, checkpoint/retry policy, and response summary before execution.

One AML request can give one Aras transaction boundary for its actions, but an HTTP request, separate SQL connection, Vault transfer, and external HTTP call are not thereby atomic. Use an outbox/job record, idempotency, compensation, or reconciliation when effects cross boundaries.

Direct SQL and `applySQL` observed in legacy source are evidence of migration risk, not permission to copy them. Prefer IOM/AML for business data and reject direct SQL writes where Aras permissions, events, lifecycle, versioning, history, or audit apply. Retain a legacy read-only query only as an explicitly approved compatibility boundary: it must be least-privilege, parameterized, bounded, isolated behind an adapter, tested against the target schema, and protected by caller authorization because SQL does not enforce Aras permissions.

## Async, cancellation, and external services

- Use asynchronous I/O where the selected library supports it, and propagate the request cancellation signal through database, stream, and outbound HTTP calls when possible.
- IOM calls are not made thread-safe by wrapping them in `Task.Run`. Do not run concurrent work against one `Innovator` or connection without a proven contract.
- Never use fire-and-forget work that captures request data, a request-scoped session, or mutable Items. The reference application has such patterns but no verified completion, cancellation, or failure-observation contract.
- Move long-running work to an explicit Agent/worker/queue boundary. Persist job identity and state, create a fresh least-privilege Aras session in the worker, make retries idempotent, and expose bounded status/cancellation semantics.
- Configure outbound clients with explicit base address/authentication, timeout, cancellation, status/body validation, redaction, and retry rules. Retry only idempotent operations or operations protected by an idempotency key; do not mix synchronous blocking with async flows.

## Files and Vault

- Validate upload presence, size, extension/content expectations, and safe display name before parsing; do not trust client filenames as filesystem paths.
- Stream large content where possible and dispose upload, Vault, archive-entry, response, and temporary-file resources deterministically. Avoid buffering an unbounded multi-file archive in memory.
- Retrieve and store managed content through authenticated Aras File/Vault APIs. A database File row or physical Vault path is not a download authorization contract.
- Sanitize response filenames and set content type/disposition deliberately. Bound batch-download file count and total bytes.
- If temporary files are unavoidable, use an isolated generated directory, deny path traversal, clean it in `finally`, and do not use a shared user-derived path.

## Configuration, logging, and diagnostics

- Bind URL, database name, credential source, timeouts, size/batch limits, Vault/external endpoints, and feature flags from environment-specific configuration. Validate required non-secret settings at startup; obtain secrets from the approved secret store and never commit their values.
- Give every request or job a correlation ID and log the failing hop, duration, sanitized operation, caller/Aras identity classification, result cardinality, dependency status, and build/hotfix. Do not log whole request arguments, uploaded content, tokens, passwords, personal data, full AML, or raw SQL values.
- Ensure logging failure cannot recursively depend on the same failing Aras path or create unobserved background tasks; provide a bounded fallback sink.
- Diagnose hop by hop: HTTP host/auth -> API binding -> service -> IOM login/request -> Innovator server -> DB/Vault/external dependency. Reproduce with the smallest safe request and one hypothesis at a time.
- Add tests for validation, permitted/denied identity, Aras Error Item, zero/one/many results, timeout/cancellation, duplicate retry, bulk rollback/partial failure, file limits/cleanup, and redaction as applicable. No project test suite was found in the reference application, so do not invent its framework.

## Dangerous assumptions

- Do not assume Release 30 server `.NET 6` defines the external Web API runtime.
- Do not assume a process-wide IOM login is request-safe, thread-safe, or valid after expiry.
- Do not assume API authentication and Aras authorization are the same boundary.
- Do not assume HTTP 200, no C# exception, or a non-null Item means the Aras operation succeeded.
- Do not assume one HTTP request makes Aras, SQL, Vault, and external calls atomic.
- Do not treat legacy direct SQL writes, interpolated AML/SQL, fire-and-forget tasks, or exception exposure as reusable conventions.
- Do not copy a business-specific endpoint or DTO when the live source can be searched cheaply.
