# Evidence policy and conflict ledger

## Source priority

Apply evidence by target release, not by publication novelty:

1. Official Aras documentation for the exact target release and hotfix.
2. Official Aras documentation for an adjacent release, explicitly labeled as an inference pending target-release confirmation.
3. User-provided training material and development notes, treated as examples and operating experience.
4. User-provided third-party summaries, treated as interpretation and troubleshooting heuristics.
5. Memory or generic .NET/web advice.

If sources conflict, quote/paraphrase both positions, decide using the highest applicable source, and state why the lower-priority source likely diverged: different release, classic versus modern client, simplified teaching language, local convention, private API, typo, or a safety recommendation that is stricter than the platform contract.

## Sources synthesized into this Skill

- Official target-release installation documentation.
- Official programming documentation for architecture, AML/IOM, and Server Event semantics.
- User-provided training material and development notes.
- User-provided third-party summaries covering architecture, deployment, AML, IOM, relationships, permissions, transactions, diagnostics, files, workflow, and UI.

The Skill is self-contained; these sources are provenance, not runtime dependencies.

## Resolved conflicts and caveats

| Topic | Lower-priority claim | Decision | Likely reason |
|---|---|---|---|
| 2024 runtime | Newer community pages may say .NET 8/Kestrel replaces older prerequisites | For 2024 install both .NET Framework 4.7.2 and ASP.NET Core/.NET Runtime + Hosting Bundle 6.0.6; IIS remains part of MSI topology | Advice copied from a newer release |
| AML boundary | “All client/server and server/database interactions go through AML” | Clients submit AML; IOM builds AML; server persists Items to mapped SQL tables. Do not treat database internals as an AML transport contract | Architectural shorthand collapsed persistence into protocol |
| Method return | Training says every server Method must return `Item` | Generic invoked Methods return an Item-shaped result; Server Event Methods have event-specific semantics. Official guide says a Server Event normally returns no replacement Item except an error | Teaching rule generalized across method types |
| CUI security | `Can Execute` is an extra security verification | It is client UX only. Permission and invariant checks must run server-side | UI capability confused with authorization boundary |
| Error handling | Throw `new Exception(ex.ToString())` or show full detail | Log protected detail; return safe `newError` with correlation ID. Use `throw;` only when the host contract requires propagation | Debug convenience was promoted to production pattern |
| Batch writes | Concatenate AML in a loop because batched Item flags can be troublesome | Build clean IOM request Items or XML nodes; never interpolate untrusted values. Batch only after bounded, transactional testing | Workaround for a specific object-state bug became a default |
| SQL | `applySQL` is a normal Innovator API and can be used after elevation | Quarantine to read-only DBA diagnostics when officially justified; never use for business writes | API catalog described availability, not architectural suitability |
| `serverEvents=0` | Use it to improve performance | Reject for normal business writes because it bypasses rules and integrations; reserve for vendor-documented administration/migration with explicit reconciliation | Performance tip ignored semantic cost |
| AML `update where=...` | Omitting `id` enables convenient multi-row updates | Do not use as a default. Verify target release, make criteria provably restrictive, test affected count, and prefer explicit IDs | Query capability presented without blast-radius controls |
| XPath | Training examples include `start-with`/`ends-with` | Standard XPath 1.0 has `starts-with` and no standard `ends-with`; verify Innovator's parser before relying on extensions | Typo plus XPath-version confusion |
| External sync in `OnAfter` | Official guide gives ERP synchronization as an example | `OnAfter` participates in Aras transaction behavior, but a remote ERP call is not magically atomic; use an outbox/idempotency pattern | Official example illustrates hook timing, not distributed transaction guarantees |
| Private client calls | Frame/DOM/grid snippets are presented as direct recipes | Mark Compatibility/Private, isolate in one adapter, and test per release | Material targets classic client internals from Aras 12 |

## Evidence statement template

Use this compact form when a claim is version-sensitive:

```text
Target: Aras Innovator <release/SP/hotfix>, <client/topology>.
Official contract: <target-release fact>.
Secondary material: <claim and source class>.
Decision: <chosen behavior>.
Compatibility test: <what proves it on this environment>.
```
