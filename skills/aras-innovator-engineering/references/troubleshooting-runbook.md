# Troubleshooting runbook

## Evidence bundle

Capture before changing configuration:

```text
Release / SP / hotfix:
Environment and topology:
UTC occurrence window:
User + effective Identity set:
URL and component hop:
Operation / ItemType / action / target ID:
Expected vs observed:
Exact safe error + correlation ID:
Relevant IIS/server/OAuth/Vault/Agent/Conversion logs:
Last known good and recent change:
Minimal reproduction:
```

Redact secrets. Keep original logs and make investigation copies.

## Hop isolation

1. **Browser/client**: console/network errors, request URL/status, response type, CUI/client event, cache.
2. **IIS/reverse proxy**: bindings, TLS, authentication roles, redirect/module/handler status, AspNetCoreModuleV2.
3. **Innovator Server**: request dispatch, Method/Event, permission, transaction, runtime config.
4. **OAuth**: discovery URL, DNS, certificate chain, password/config, clock.
5. **SQL**: connectivity, login role, database/code-tree version match, blocking/timeouts.
6. **Vault**: endpoint, storage permission/capacity, file metadata, certificate.
7. **Agent/Conversion**: service identity, unique alias, port, queue/job state, dependency runtime, capacity.
8. **External system**: timeout, idempotency, retry/dead-letter, contract/schema.

## Symptom map

| Symptom | First checks | Avoid |
|---|---|---|
| `500.21` | IIS roles/handler/runtime registration and install order | Running a legacy registration command without identifying the handler |
| `401` after login | IIS Windows Authentication role and effective auth settings | Broad anonymous access as a workaround |
| Tear-off `404` | extensionless URL handling and IIS modules | Client DOM hacks |
| Grid missing columns / XML comment error | XML parser/component compatibility, returned AML | Editing database XML directly |
| Cookie/login anomaly | hostname characters, especially underscore; domain/path/SameSite | Reusing invalid alias |
| `AspNetCoreModuleV2` `500` | Hosting Bundle 6.0.6 install/repair for 2024 | Assuming .NET 8 substitutes for target runtime |
| Redirect loop | HTTP Redirect module and proxy/HTTPS rules | Adding more redirects blindly |
| OAuth discovery inaccessible | external hostname, DNS, TLS trust, password without spaces, copied certs | `localhost` across hosts |
| Unauthorized update still succeeds | Permission/lifecycle/elevation/Event path; direct AML negative test | Trusting hidden CUI button |
| Relationship data wrong | source vs Relationship Item vs related Item ownership | Writing quantity onto related Item |
| Duplicate external action | outbox/idempotency/retry history | Retrying synchronous `OnAfter` call blindly |
| File not found | File Item, Vault URL, permission, storage/capacity, restore consistency | Using physical Vault path as contract |
| Works only in one release/client | private frame/grid/DOM call or changed public API | Spreading conditional hacks across Methods |

## Method/Event debugging

1. Confirm binding context and event stage.
2. Inspect sanitized input AML and effective caller Identity.
3. Determine whether the Item is single, collection, error, result, or logical.
4. Test public IOM operation in isolation with minimal `select`.
5. Disable neither events nor permissions to “see if it works” in production.
6. In local development only, enable the documented debug facility/attach to the correct worker process. Remove `Debugger.Break/Launch` and disable debug compilation for production.
7. Verify error details are logged server-side and the client receives only safe information.

## Performance diagnosis

- Measure request duration, returned Item count, payload size, relationship depth, SQL duration/blocking, Method/Event time, and external call time separately.
- Reduce `select`; add paging; replace broad `//` XPath; bound recursive relationships.
- Find repeated per-row AML calls (N+1). Batch reads/writes only after semantics are tested.
- Do not use direct SQL or disable events as the first optimization.
- Co-located Conversion can starve the Innovator host; verify CPU/memory/queue evidence.

## Experiment log

For each change record:

```text
Hypothesis:
Observation supporting it:
Single controlled change:
Result and evidence:
Rollback performed/available:
Regression test added:
```

Stop when evidence contradicts the hypothesis; do not stack untracked configuration changes.
