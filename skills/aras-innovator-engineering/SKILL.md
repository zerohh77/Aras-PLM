---
name: aras-innovator-engineering
description: Use when designing, coding, reviewing, installing, upgrading, integrating, securing, or debugging Aras Innovator, especially AML/IOM, ItemTypes, Relationships, Methods, Server Events, CUI, Vault, OAuth, Agent, Conversion Server, IIS, SQL Server, permissions, transactions, packages, or release compatibility.
---

# Aras Innovator Engineering

## Purpose

Produce release-aware Aras solutions that preserve server-side authorization, transaction integrity, upgradeability, and operational evidence. Treat examples from training decks, blogs, and remembered APIs as candidates to verify—not as production contracts.

## Start every task with this gate

1. Identify the exact Innovator release, service pack/hotfix, deployment shape, and execution layer. For advisory/design/code requests, never pause merely because version details are missing: state a bounded assumption, give the safe version-neutral path, and mark signatures that need target-release verification. Ask only before an actual mutation whose safe scope cannot be resolved.
2. Classify the task: `install/upgrade`, `model/configure`, `query/write`, `server method/event`, `client/CUI`, `file/Vault`, `integration`, or `diagnose`.
3. Apply the evidence order in [evidence-policy.md](references/evidence-policy.md).
4. Label every proposed mechanism:
   - `Stable`: documented configuration or public AML/IOM behavior for the target release.
   - `Compatibility`: classic-client or older-release behavior that needs a release adapter and regression test.
   - `Private`: internal DOM/frame/grid/database implementation; isolate behind one adapter and never present as a stable API.
   - `Reject`: bypasses security, transaction, audit, or recovery boundaries.
5. Prefer, in order: configuration/metadata → public IOM/AML → documented extension point → isolated compatibility adapter. Never choose direct SQL or private UI internals merely because they are shorter.

## Non-negotiable constraints

- The browser is not a trust boundary. CUI `Can Execute`, hidden/read-only fields, and client validation are UX only; enforce permission and business validation on the server, then test a direct AML/API call as an unauthorized identity.
- Perform business writes through Item actions using public IOM/AML. Do not write Aras business tables with `applySQL`, stored procedures, or ad-hoc SQL.
- Never interpolate untrusted data into AML, SQL, XPath, HTML, or URLs. Build Items/properties or XML nodes; if legacy string AML is unavoidable, XML-escape every value and keep the builder centralized and tested.
- Do not use `serverEvents="0"` for ordinary business writes. It can bypass validation, lifecycle, audit, and integration behavior.
- Privilege elevation is last resort: name the Identity, narrow the protected block, restore in `finally`, record why it is needed, and add a negative authorization test. Elevation must not compensate for a wrong permission model.
- Return safe, actionable errors to users; keep stack traces, paths, SQL, tokens, and full AML in protected server logs. Do not `throw new Exception(ex.ToString())` or expose `getErrorDetail()` wholesale.
- Do not assume a database transaction atomically covers email, ERP, message queues, or other remote side effects. Use an outbox/idempotency key, retry policy, and compensation/reconciliation.
- Store and retrieve managed files through Vault APIs. Never depend on a Vault file's physical path as an application contract.
- Bound every query: explicit `select`, restrictive criteria, paging/maxRecords, and bounded relationship depth. Avoid recursive/unbounded AML and broad `where` updates.
- Keep database, code tree, and release/hotfix level matched. Never treat the 2024 installer as an upgrade mechanism.
- Keep secrets, passwords, certificate private keys, internal hostnames, user data, and real GUIDs out of source, logs, examples, and packages.
- Never place placeholder raw AML concatenation inside an error-handling template. A sample that teaches error handling must use IOM or a named operation boundary so it does not normalize a second unsafe pattern.

## Pressure-trap responses

- **CUI/security request:** lead with Permission/lifecycle authorization, classify any `top`/frame/grid call as Compatibility/Private, and include an unauthorized direct AML test. Do not invent a CUI return shape or remove inherited permissions without an impact review.
- **Exception template request:** use a proven logging adapter, return `inn.newError` with a correlation ID, and explicitly say the sink/ACL/rotation must be verified. Do not answer with `System.Diagnostics.Trace` as though it is automatically wired; do not throw a sanitized replacement exception when an Aras Error Item is the contract.
- **Urgent bulk update:** answer directly. Reject `applySQL` business writes, concatenated AML, routine elevation, and `serverEvents="0"`. Provide: dry-run exact IDs/count, backup old values, clean IOM Item actions in bounded batches, per-batch audit/checkpoint, retry/resume, post-validation, and rollback. Never say SQL may be enabled later for performance.
- **Conflicting install versions:** separate official target-release requirements from generic hardening. Do not add a generic recommendation to an “official minimum” checklist unless labeled as such.

## Choose the implementation layer

Use [architecture-and-data-flow.md](references/architecture-and-data-flow.md) for the full map.

| Need | Preferred layer | Required verification |
|---|---|---|
| Data shape, forms, lifecycle, permissions | ItemType/Property/RelationshipType/Form/Lifecycle/Permission/CUI configuration | Package export, least-privilege identity matrix |
| Query or business write | Public IOM building AML Item actions | `isError`, cardinality, select/depth bounds, unauthorized test |
| Invariant or cross-client rule | Server Event/Server Method | event stage, rollback behavior, idempotency, server-side test |
| Convenience interaction | Client Method/CUI | server duplicate of validation, classic/modern compatibility |
| File content | File Item + Vault | permission, checkout/download path, capacity and backup |
| Background conversion/replication | Agent/Conversion Server | separate capacity, service account, port, retry/observability |
| External system | Server integration boundary + outbox | idempotency, retry, timeout, compensation |

## Coding workflow

1. Model first: identify source Item, Relationship Item, related Item, lifecycle state, permission, and package ownership.
2. Define the request contract: exact ItemType/action, required properties, expected single/collection/error/result response, and cardinality.
3. Build with IOM Items and `setProperty`/`setAttribute`; use raw AML only where it makes hierarchy clearer.
4. Query minimally: set `select`; include `related_id(...)` only when needed; bound relationships and pagination.
5. Place validation at the server boundary. Client validation may improve feedback but must not be the only check.
6. For Server Events, select the stage deliberately:
   - `OnBefore*`: validate or transform request AML; returning an error stops the action.
   - `On*`: replace standard behavior only when explicitly intended and fully tested.
   - `OnAfter*`: process the response while still respecting transaction/rollback semantics; defer irreversible remote side effects.
7. Handle `Item` result shapes before reading values: error → collection count/cardinality → property extraction.
8. Add tests for permitted, denied, malformed, empty, multiple-result, retry, and rollback paths.
9. Package configuration and Methods; document target release and private/compatibility dependencies.

Use [modeling-and-development.md](references/modeling-and-development.md), [security-and-transactions.md](references/security-and-transactions.md), and [code-recipes.md](references/code-recipes.md) while implementing.

## Installation and upgrade workflow

For 2024 Release, follow [installation-2024.md](references/installation-2024.md) exactly.

1. Confirm this is a new install or a separately governed upgrade/migration.
2. Verify OS/IIS/.NET/Hosting Bundle/VC++/SQL prerequisites before running the installer.
3. Record topology, DNS names, TLS certificates, ports, service accounts, SQL accounts, MAC-bound license, Vault capacity, and backups.
4. Use non-underscore hostnames and trusted certificates. Confirm OAuth discovery from every consuming host.
5. Create separate owner and regular DB logins; do not use `sa` as the application account.
6. Set `CorporateTimeZone` before production use; change default admin credentials.
7. Smoke-test login, direct CRUD authorization, Vault upload/download, OAuth discovery, mail, Agent jobs, and Conversion only if installed.
8. Preserve the exact installer media and create a coordinated backup/restore runbook for database, Vault, configuration, keys, and certificates.

## Diagnosis workflow

Use [troubleshooting-runbook.md](references/troubleshooting-runbook.md). Do not start by changing code.

1. Freeze evidence: release/SP/hotfix, UTC timestamp, URL, user/Identity, correlation ID, request shape with secrets removed, server/IIS/OAuth/Agent logs, and last known change.
2. Classify the failing hop: browser → IIS/reverse proxy → Innovator Server → OAuth/DB/Vault/Agent/Conversion/external service.
3. Reproduce with the smallest safe request and a known authorization matrix.
4. Test one hypothesis at a time; record observation, change, result, and rollback.
5. Use browser developer tools for client issues and server logging for server issues. Attach a debugger only in an isolated development environment.
6. After fixing, add a regression test and document any compatibility/private API dependency.

## Output contract

For architecture, code, review, or diagnosis requests, return:

1. `Release assumptions`
2. `Evidence classification` for version-sensitive claims
3. `Data flow and chosen layer`
4. `Implementation` with public APIs first
5. `Security/transaction boundary`
6. `Verification matrix`
7. `Rollback or recovery`
8. `Compatibility debt`, if any

Do not claim a code sample is copy-ready unless target ItemType/property names, permission model, release, event stage, and failure behavior are explicit.

## Reference routing

- Source priority, conflict decisions, and provenance: [evidence-policy.md](references/evidence-policy.md)
- Core architecture, module dependencies, and design philosophy: [architecture-and-data-flow.md](references/architecture-and-data-flow.md)
- Exact 2024 installation constraints: [installation-2024.md](references/installation-2024.md)
- Items, AML/IOM, Relationships, Methods, Events, client, CUI: [modeling-and-development.md](references/modeling-and-development.md)
- Permissions, elevation, transactions, external effects, logging: [security-and-transactions.md](references/security-and-transactions.md)
- Symptom-first diagnosis: [troubleshooting-runbook.md](references/troubleshooting-runbook.md)
- Safe implementation templates: [code-recipes.md](references/code-recipes.md)
- Classic/private API quarantine: [legacy-compatibility.md](references/legacy-compatibility.md)
- RED/GREEN evaluation record: [evaluations.md](references/evaluations.md)
