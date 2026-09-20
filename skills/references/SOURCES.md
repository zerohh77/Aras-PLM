# Aras Release 30 Source Index

Target: Aras Innovator Release 30, build `14.0.22.40048`. This is an evidence index, not a copied manual.

## Release and hotfix identity

- [Official Aras Innovator Platform documentation library](https://www.aras.com/community/DocumentationLibrary/Library/Aras%20Innovator%20Platform.htm)
  - Scope: Release 30 documentation catalog
  - Supports: official document set and listed hotfix `068423.00`
  - Confidence: High
- [Official Upgrading to 31 from Aras Innovator 14+](https://www.aras.com/community/DocumentationLibrary/ALL%20PDFs/Flare%20PDF/Flare%20PDF/Innovator%2031/Aras%20Innovator%2031%20-%20Upgrading%20to%2031%20from%20Aras%20Innovator%2014%2B.pdf)
  - Scope: upgrade eligibility table
  - Supports: Release 30 maps to build `14.0.22.40048`
  - Confidence: High
## Runtime and browser compatibility

- [Official Release 30 Platform Specifications](https://www.aras.com/community/DocumentationLibrary/ALL%20PDFs/Flare%20PDF/Flare%20PDF/Innovator%2030/Aras%20Innovator%2030%20-%20Platform%20Specifications.pdf)
  - Scope: Release 30
  - Supports: .NET/Hosting Bundle requirements and supported OS/browser matrix
  - Confidence: High
- [Official Release 30 Programmer's Guide](https://www.aras.com/community/DocumentationLibrary/ALL%20PDFs/Flare%20PDF/Flare%20PDF/Innovator%2030/Aras%20Innovator%2030%20-%20Programmer%27s%20Guide.pdf)
  - Scope: Release 30
  - Supports: .NET 6 server runtime, custom DLL deployment, IOM Item semantics, action/event behavior, client execution contexts, and API-specific Promise examples
  - Confidence: High
  - Gap retained: it does not establish a general Method C# language version or general async/threading contract

## Item actions, events, and relationships

- [Official Release 30 Programmer's Guide](https://www.aras.com/community/DocumentationLibrary/ALL%20PDFs/Flare%20PDF/Flare%20PDF/Innovator%2030/Aras%20Innovator%2030%20-%20Programmer%27s%20Guide.pdf)
  - Scope: Release 30
  - Supports: `apply` versus `loadAML`, `edit`/`update`/`version`, event stages, `event_version` 1/2, `serverEvents`, Item/collection/error shapes, and relationship APIs
  - Confidence: High
- [Official Release 30 Life Cycles](https://www.aras.com/community/DocumentationLibrary/ALL%20PDFs/Flare%20PDF/Flare%20PDF/Innovator%2030/Aras%20Innovator%2030%20-%20Life%20Cycles.pdf)
  - Scope: Release 30
  - Supports: lifecycle-state permissions, transition behavior, and RelationshipType/lifecycle Item Behavior interactions
  - Confidence: High

## Files and Vault

- [Official Release 30 File Handling](https://www.aras.com/community/DocumentationLibrary/ALL%20PDFs/Flare%20PDF/Flare%20PDF/Innovator%2030/Aras%20Innovator%2030%20-%20File%20Handling.pdf)
  - Scope: Release 30
  - Supports: File Item immutability, non-versionability, container-derived permissions, and Vault/UI boundary
  - Confidence: High

## Known issues and packaging

- [Official Release 30 Release Notes](https://www.aras.com/community/DocumentationLibrary/ALL%20PDFs/Flare%20PDF/Flare%20PDF/Innovator%2030/Aras%20Innovator%2030%20-%20Release%20Notes.pdf)
  - Scope: Release 30
  - Supports: TGV/CUI export dependencies, Boolean access-control `NULL` caveat, browser/UI known issues, and vendor incident workarounds
  - Confidence: High

## Repository and secondary evidence

- Mature Core Skill and its focused references in `skills/aras-release30-core/`
  - Scope: existing repository knowledge base, previously synthesized from official documents and sanitized training/development materials
  - Supports: architecture, AML/IOM patterns, security/transaction constraints, safe recipes, compatibility quarantine, and troubleshooting
  - Confidence: High for rules explicitly bounded to Release 30; otherwise follow its evidence labels
- Validated reference Web API implementation and hosting configuration
  - Scope: classic ASP.NET Web API application targeting .NET Framework 4.7.2, reviewed by targeted source searches with generated `bin`/`obj` content excluded
  - Supports: hosting model, route/filter composition, IOM reference boundary, configuration access, and absence of a discovered Web API test project
  - Confidence: High for observed source; exact Release 30 IOM assembly provenance remains unresolved
- Validated reference Web API connection and Aras integration boundaries
  - Scope: shared connection service, per-operation connection wrapper, configuration-backed connection creation, and targeted searches for login, HTTP principal, authorization, and Identity impersonation
  - Supports: dominant configured-account shared session, disposable per-operation wrapper, one explicit user-session path, endpoint-specific caller-to-Aras identity, and absence of a uniform source-level HTTP-principal or impersonation layer
  - Confidence: High for identity-path classification and abstraction ownership; Low for thread safety or session reuse because no contract/test proves them
- Validated reference Web API representative import/bulk flow
  - Scope: one controller-to-service import path using pre-validation, parameterized bounded SQL reads, an in-memory IOM action plan, and one `applyAML` write
  - Supports: thin HTTP boundary as a preferred local direction, validate-before-write, bounded lookup batches, explicit result checking, and one Aras write boundary
  - Confidence: High for that flow; Medium as a project-wide convention because older counterexamples remain
- Validated reference Web API error, async, SQL, file, and outbound-integration searches
  - Scope: global action filter/response helpers, async and `Task.Run` call sites, `applySQL`/database access, upload/download/Vault streams, outbound HTTP, authentication markers, and tests
  - Supports: mixed HTTP/error semantics, direct-SQL migration risk, missing cancellation contract, fire-and-forget risk, stream disposal/size concerns, inconsistent outbound timeout/retry behavior, no discovered source-level API authorization filter, and no discovered test project
  - Confidence: High for source observations; these legacy patterns are evidence for guardrails, not endorsed conventions
