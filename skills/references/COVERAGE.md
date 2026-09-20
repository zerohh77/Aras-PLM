# Aras Release 30 Knowledge Coverage

Target: Aras Innovator Release 30, build `14.0.22.40048`.

| Topic | Status | Depth | Skill Destination | Notes |
|---|---|---:|---|---|
| Core Item Model | Covered | High | core | Existing mature Core checked |
| AML actions | Covered | High | core/server-csharp | Release 30 semantics checked |
| IOM result semantics | Covered | High | core/server-csharp | Request/response and cardinality checked |
| Relationships | Covered | High | core/server-csharp | Row identity and manipulation covered |
| Versioning | Covered | High | core | High-risk Release 30 behavior checked |
| Server Events | Covered | High | core/server-csharp | Stages and event versions covered |
| Lifecycle | Covered | Medium | core | Configuration-sensitive behavior retained in Core |
| Permissions | Covered | Medium | core/server-csharp | Elevation signature remains release/runtime-sensitive |
| Transactions | Covered | High | core/server-csharp/webapi-csharp | Aras, HTTP, SQL, Vault, and external boundaries distinguished |
| Direct SQL | Covered | High | core/server-csharp/webapi-csharp | Business writes rejected; bounded read-model exception documented |
| Workflow | Partial | Low | core | No current project usage to prioritize |
| Vault / Files | Covered | Medium | core | Immutability, container permission, Vault boundary |
| Server C# Runtime | Partial | Medium | server-csharp | .NET 6 verified; Method compiler language version unresolved |
| Server C# Patterns | Covered | High | server-csharp | Operational patterns derived from Core |
| Server async/threading | Unresolved | Low | server-csharp | No general request-Method guarantee verified |
| Client JS Runtime | Partial | Medium | client-js | Supported browser floor known; ECMAScript level not specified |
| Client Contexts | Covered | High | client-js | Documented Item/Form/Grid/Field contexts |
| Browser Compatibility | Covered | Medium | client-js | Release 30 platform matrix |
| Client async dispatch | Unresolved | Low | client-js | Only API-specific Promise behavior verified |
| Hotfix `068423.00` effects | Unresolved | Low | core | Presence indexed; behavioral impact not established |
| Web API Runtime Compatibility | Partial | Medium | webapi-csharp | Reference app targets .NET Framework 4.7.2; exact Release 30 IOM provenance/runtime support unresolved |
| Web API Architecture | Partial | Medium | webapi-csharp | Hosting and full request chain verified; controller/service boundaries are mixed |
| Aras Connection Lifetime | Partial | Medium | webapi-csharp | Shared configured-account gateway and disposable per-operation wrapper identified; thread safety and reuse contract unresolved |
| Web API IOM/AML Patterns | Covered | Medium | webapi-csharp | Item construction, response checks, bounded single-AML import pattern verified; legacy counterexamples retained as debt |
| HTTP ↔ Aras Error Mapping | Partial | Medium | webapi-csharp | Safe correlation pattern exists, but HTTP status and exception exposure are inconsistent |
| Bulk Operations | Partial | Medium | server-csharp/webapi-csharp | Bounded reads and planned single AML apply verified; other flows use unsafe concurrency/direct SQL |
| SQL / Data Access | Covered | Medium | webapi-csharp | Parameterized bounded reads exist; legacy interpolated reads/writes are explicitly not conventions |
| Async / Cancellation | Unresolved | Low | webapi-csharp | No CancellationToken flow; sync blocking and fire-and-forget patterns exist |
| Long-running APIs | Unresolved | Low | client-js/webapi-csharp | No verified durable job/queue lifecycle in reference application |
| Web API File Handling | Partial | Medium | webapi-csharp | Vault streams and HTTP stream responses exist; memory/temp bounds and cancellation are inconsistent |
| API Caller → Aras Identity Mapping | Covered | Medium | webapi-csharp | Endpoint-specific: configured technical account dominates, with an explicit user-session path; no uniform HTTP-principal mapping found |
| Web API Configuration | Partial | Medium | webapi-csharp | Environment configuration access verified; secret lifecycle/startup validation not established |
| External HTTP Integrations | Partial | Low | webapi-csharp | Calls exist; timeout, cancellation, reuse, retry, and redaction conventions are not consistent |
| Logging / Diagnostics | Partial | Medium | webapi-csharp | Logging and correlation pattern exist; request/exception exposure and background sink remain risks |
| Error Handling | Covered | Medium | core/server-csharp/client-js/webapi-csharp | Cross-layer response classification and safe outward errors covered |
| Testing | Partial | Low | all | Verification matrices exist; no Web API test project found in reference source |
| Federation | Not researched | None | - | No current project relevance established |
