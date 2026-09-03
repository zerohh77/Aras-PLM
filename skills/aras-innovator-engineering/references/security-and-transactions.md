# Security, transactions, and operational safety

## Authorization model

Authorization is server-side and Identity-based. Evaluate effective permissions across Item Permission, lifecycle-state permissions, ownership/creator rules, and any event logic. A visible button does not prove authorization; a hidden button does not prevent an API call.

For every protected action, test at least:

| Identity | UI | Direct AML/API | Expected |
|---|---|---|---|
| authorized | enabled | succeeds | pass |
| authenticated but unauthorized | hidden/disabled | denied | pass |
| unrelated/least-privilege | absent | denied without data leak | pass |

Do not “fix” a permission failure by broadening World/All Employees or by silently elevating.

## Validation placement

- Client validation: immediate feedback only.
- `OnBefore*` Server Event: authoritative input/invariant validation before persistence.
- Database constraints: last-resort structural integrity owned by a controlled schema strategy; do not introduce unmanaged constraints casually.
- External validation: timeout-bound and failure-mode aware; avoid synchronous dependence when availability differs from Innovator.

Return domain-safe messages. Log technical detail with a correlation ID and access controls.

## Privilege elevation

If target-release public APIs require elevation:

1. Prove the ordinary caller must not receive the permission permanently.
2. Use a dedicated, least-privilege Identity—not Administrators by default.
3. Elevate only around the exact operation.
4. Restore/revoke in `finally` even on error.
5. Validate all inputs before elevation.
6. Audit caller, action, target IDs, result, and correlation ID without secrets.
7. Test denied caller, forged ID, partial failure, and cleanup.

API names for granting/revoking identity have changed across releases; verify the target release instead of copying `GrantIdentity`/`RevokeIdentity` or older permission helpers blindly.

## Transactions

Item actions and Server Events participate in Aras-managed transaction behavior. Do not issue manual commit/rollback against Innovator's database connection. An `OnAfter*` error can roll back the Aras transaction, but that does not roll back a remote HTTP call, sent email, or external database mutation.

### External side-effect pattern

Use an outbox Item in the same Aras transaction:

```text
Business action
  -> validate
  -> write business Items + Integration Outbox Item atomically
  -> commit
  -> Agent/background worker claims outbox
  -> call external service with idempotency key
  -> mark completed, or retry with bounded backoff
  -> dead-letter + reconciliation after threshold
```

The idempotency key should be stable for one logical event, e.g. `<item-id>:<generation>:<event-type>`. Store attempt count, next attempt, last safe error, and correlation ID. Never assume “OnAfter” alone provides exactly-once delivery.

## Dangerous bypasses

### `serverEvents="0"`

This can suppress validation, lifecycle/workflow integration, derived data, audit, and outbound triggers. Reject for normal product code. If a vendor-documented migration/repair requires it, demand:

- maintenance window and backup;
- exact target list and row count;
- dry run;
- explicit revalidation/recalculation/reindex/reconciliation;
- immutable audit of operator and affected IDs;
- rollback plan.

### Direct SQL / `applySQL`

Do not use for business writes. Read-only SQL diagnostics belong to a DBA-controlled, least-privilege workflow with sanitized parameters, execution-plan awareness, time bounds, and no secret/customer-data leakage. Even reads can bypass Aras permissions and expose protected data.

### Raw `where`

`where` may expose SQL-like expressiveness and injection/blast-radius hazards. Prefer Item properties/conditions. If unavoidable and documented for the target release, use only trusted, fixed expressions with separately validated values; first retrieve and review exact IDs, then update explicit IDs.

## Error and log policy

User-facing response may contain:

- stable error code/correlation ID;
- concise domain message;
- safe corrective action.

Protected logs may contain:

- UTC timestamp, release/build, component, method/event, caller Identity;
- correlation ID and target Item IDs;
- sanitized error string and stack trace;
- duration and retry count.

Do not log or return:

- passwords, tokens, certificate private keys;
- connection strings;
- full raw AML containing sensitive properties;
- unrestricted SQL;
- internal filesystem paths or personal/internal hostnames unless access-controlled and necessary.

Use the logging facility actually configured for the target Innovator release. `System.Diagnostics.Trace` is acceptable only when its sink and retention are proven; otherwise it can silently disappear.

## Recovery boundary

A recoverable Innovator environment includes:

- SQL database;
- Vault storage;
- Innovator, Vault, OAuth, Agent, and Conversion configuration;
- certificates/keys and protected secrets;
- license/install media and exact code tree;
- package/source history.

Backups with independent timestamps are not a proven recovery. Test a coordinated restore and validate database/Vault references, OAuth discovery, login, and file retrieval.
