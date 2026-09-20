---
name: aras-release30-core
description: Use for Aras Innovator Release 30 platform semantics, architecture, configuration, installation, security, transactions, lifecycle, workflow, Vault, packaging, integration boundaries, and cross-layer diagnosis. Use the server-csharp, webapi-csharp, or client-js specialization for implementation details.
---

# Aras Release 30 Core

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

## Release 30 / build 14.0.22.40048 compatibility boundary

Apply this section only when the target is **Aras Innovator Release 30, build 14.0.22.40048**. Confirm the build in the deployed instance and record whether Release 30 hotfix `068423.00` is installed; do not generalize these rules to every 14.x build or infer hotfix behavior without its release note or a runtime test.

- **Server runtime:** Release 30 server components run on .NET 6.0. A custom DLL used by a Server Method must target .NET 6.0, reference the IOM assembly shipped with this exact release, be deployed with its symbols to `Server/bin`, and be registered in `Method-Config.xml` with the matching namespace/template and `line_number_offset`.
- **C# compiler boundary:** .NET 6 runtime support does not establish the C# language version accepted by the Method compiler. Until `LangVersion` or an equivalent compile probe is verified on the target, follow the syntax already accepted by its Method template and compile-test newer constructs such as records, nullable-reference annotations, target-typed `new`, switch expressions, and `using var`. Do not teach general `async`/threading in request Server Methods as supported merely because specialized APIs use tasks or worker threads.
- **IOM response semantics:** `Item.apply()` sends the request Item DOM and returns a new response `Item`; keep request and response variables separate. Distinguish error, zero matches, one result, and multiple results before reading properties. `loadAML()` instead replaces the current Item DOM.
- **Action and event semantics:** `update` requires a lock; `edit` performs lock/update/unlock; a versionable first update after locking versions unless `version="0"`; `version` creates a new generation and has its own version/update event sequence. `serverEvents="0"` is not a complete event bypass: required events still run, and edit-related lock events can still run. Treat `On*` as replacement behavior, not an extra hook.
- **event_version boundary:** In event version 2, grouped `onAfterAdd`, `onAfterUpdate`, and `onAfterVersion` handling runs once for the request group with the result collection as context, rather than once per Item as in version 1. Version 2 also changes copy/version behavior for relationship rows; therefore inspect the Method's event version and test multi-ID requests before relying on per-item execution.
- **Relationship versioning:** A relationship row is an Item with its own identity and properties. Source-item versioning/cloning can clone relationship rows, while which related generation is referenced depends on RelationshipType behavior plus lifecycle-state behavior. Inspect both configurations; never infer fixed/float behavior from names or from one environment.
- **Client browser floor:** Test client code across the documented Release 30 matrix: Windows 10/11 with Edge, Firefox ESR 102/115, or Chrome 119 minimum; Windows 8.1 with Firefox ESR 102/115; macOS 10.15 with Firefox ESR 102/115 or Chrome 119 minimum.
- **Client context:** For documented Release 30 handlers, Item Actions receive the Item as `this`; Form/Grid events receive the browser document DOM; Field events receive the Field object; Form/Grid/Field code obtains the current Item through `document.thisItem`; relationship-grid code uses `parent.thisItem`. Grid callback IDs may be empty when no related Item exists. Keep any deeper frame, DOM, or grid access behind a Compatibility/Private adapter.
- **Client async boundary:** Promise use is supported only where the called API documents it (for example, documented Vault file selection and asynchronous apply flows). Do not assume an Aras event dispatcher awaits a Promise returned by an arbitrary Client Method; prove the specific caller contract and failure propagation in every supported browser.
- **File boundary:** File Items are immutable and non-versionable; replace the File and version its container instead of updating File content. File access derives from container relationships, and a database row alone does not prove that content is downloadable from Vault.
- **Release 30 known-risk checks:** Export TGV-related CUI/Presentation Configuration dependencies explicitly when packaging; set Boolean access-control values explicitly to `0` or `1` rather than depending on `NULL`; test relationship-grid behavior in each supported browser. Treat vendor-documented database repair workarounds as incident procedures, not permission for routine direct SQL.

Source basis: the official Release 30 Programmer's Guide, Platform Specifications, Life Cycles, File Handling, Release Notes, and the official documentation-library hotfix index. If a local runtime contradicts a guide, capture the exact build/hotfix and reproduce before changing this boundary.

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
7. Keep request and response Items separate after `apply()`, then handle response shapes before reading values: error → zero/one/many cardinality → property extraction.
8. Add tests for permitted, denied, malformed, empty, multiple-result, retry, and rollback paths.
9. Package configuration and Methods; document target release and private/compatibility dependencies.

Use [modeling-and-development.md](references/modeling-and-development.md), [security-and-transactions.md](references/security-and-transactions.md), and [code-recipes.md](references/code-recipes.md) while implementing.

## Installation and upgrade workflow

For Release 30/build 14.0.22.40048, use the exact Release 30 Installation Guide and Platform Specifications. [installation-2024.md](references/installation-2024.md) is a 2024-only reference and must not be used as the Release 30 prerequisite or upgrade contract.

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

- Cold, uncertain, or high-risk topic: inspect [COVERAGE.md](../references/COVERAGE.md), then [SOURCES.md](../references/SOURCES.md), before opening original evidence.
- Source priority, conflict decisions, and provenance: [evidence-policy.md](references/evidence-policy.md)
- Core architecture, module dependencies, and design philosophy: [architecture-and-data-flow.md](references/architecture-and-data-flow.md)
- 2024-only installation constraints (not the Release 30 contract): [installation-2024.md](references/installation-2024.md)
- Items, AML/IOM, Relationships, Methods, Events, client, CUI: [modeling-and-development.md](references/modeling-and-development.md)
- Permissions, elevation, transactions, external effects, logging: [security-and-transactions.md](references/security-and-transactions.md)
- Symptom-first diagnosis: [troubleshooting-runbook.md](references/troubleshooting-runbook.md)
- Safe implementation templates: [code-recipes.md](references/code-recipes.md)
- Classic/private API quarantine: [legacy-compatibility.md](references/legacy-compatibility.md)
- RED/GREEN evaluation record: [evaluations.md](references/evaluations.md)
