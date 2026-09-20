---
name: aras-release30-client-js
description: Use when writing, reviewing, or debugging Aras Innovator Release 30 build 14.0.22.40048 Client Methods and browser JavaScript, including Item/Form/Field/grid/CUI contexts, client AML/IOM, dialogs, refresh, async UX, browser compatibility, and DOM/private API boundaries. Do not use as a generic JavaScript guide.
---

# Aras Release 30 Client-side JavaScript

## Scope

Implement browser-side behavior for **Aras Innovator Release 30, build 14.0.22.40048**. Client code is presentation and interaction; permissions and business invariants remain server-side.

Before coding, identify the binding (Item Action, Form, Grid, Field, relationship grid, CUI/toolbar, or dialog callback), supported browsers, new/edit/read-only state, and whether the caller expects a synchronous return value.

For a cold, uncertain, or high-risk question, inspect [COVERAGE.md](../references/COVERAGE.md) and then [SOURCES.md](../references/SOURCES.md); do not load them for routine coding.

## Browser and JavaScript boundary

Test against the documented Release 30 matrix:

- Windows 10/11: Edge, Firefox ESR 102/115, Chrome 119 minimum.
- Windows 8.1: Firefox ESR 102/115.
- macOS 10.15: Firefox ESR 102/115 or Chrome 119 minimum.

Aras does not publish an ECMAScript language-level contract for every client execution surface. Use syntax already exercised by the deployment or transpile within the project's proven build path; test newer syntax and APIs in every supported browser before adoption.

## Execution contexts

Use the documented binding rather than a universal `this` assumption:

| Binding | Documented context |
|---|---|
| Item Action | `this` is the Item |
| Form event | `this` is the browser document DOM |
| Grid event | `this` is the browser document DOM |
| Field event | `this` is the Field object |
| Form/Grid/Field current Item | `document.thisItem` |
| Relationship grid current source Item | `parent.thisItem` |

Grid callback `relationshipID` or `relatedID` values can be empty when the corresponding Item does not exist. Validate them before lookup or server calls.

`document.thisItem` and `parent.thisItem` are stable only in the documented bindings above. `top.aras`, `parent.aras`, frame traversal, hard-coded iframe IDs, grid internals, cache mutation, and Aras-owned DOM selectors are Compatibility/Private unless the exact caller contract proves them.

## Context adapter

Keep binding discovery at one boundary and pass dependencies into business UI logic:

```text
documented handler
  -> resolve context Item + aras API + optional grid/form handle
  -> validate the expected binding
  -> call product-owned function with explicit arguments
```

Fail closed with a useful compatibility error when the binding is absent. Do not scatter `top`, `parent`, or frame chains through feature code.

## Client AML/IOM and server authority

- When `this` is an Item, use its documented Innovator context where available. Otherwise obtain the API from the binding contract, not from guessed window ancestry.
- Keep request and response Items separate after `apply()`. Check Error Item and result cardinality before reading properties or refreshing the UI.
- Build Item requests/property values rather than concatenating AML strings. Bound queries and selected properties just as server code does.
- Client validation may improve feedback but must be duplicated at the authoritative server boundary. Test the same operation by direct AML/API as an unauthorized or malformed caller.

## CUI, dialogs, and refresh

- Prefer Form, CUI, and documented Aras APIs over direct DOM changes. `Can Execute`, visibility, disabled state, and read-only controls are UX, not authorization.
- Treat dialog options, callback shape, toolbar context, and refresh APIs as signature-sensitive. Verify the Release 30 caller contract and cancellation path before publishing code.
- Refresh only the affected Item/form/grid through its documented API. Do not mutate `itemsCache` or reload the whole window to hide stale state unless an isolated compatibility adapter owns that behavior.
- TGV-related CUI, Presentation Configuration, Item Presentation Configuration, and associated Command Bar objects may require explicit package export; test the imported package in a clean environment.

## Async and long-running operations

- Use Promises only where the specific API documents them, such as documented Vault selection or asynchronous apply flows.
- Do not assume an arbitrary Client Method dispatcher awaits a returned Promise or propagates its rejection. Prove the caller contract; otherwise keep the handler synchronous and hand off asynchronous completion explicitly.
- For long-running work, show cancellable/busy state, prevent accidental duplicate submission, attach a correlation or job ID, poll with a bound interval when supported, surface safe failure, and restore UI state in every completion path.
- Never keep a browser request open merely to perform server work that belongs in Agent/background processing.

## Diagnostics

- Capture build/hotfix, browser/version, binding, Item state, current Item ID/configuration, callback arguments, network request/result shape, and console error without secrets.
- Reproduce across the supported browser matrix and new/edit/read-only, main grid, relationship grid, and tear-off contexts that the feature actually supports.
- Classify every use of frame, DOM, grid, cache, or undocumented API as Compatibility/Private and give it an owner, feature detection, regression test, and removal plan.

## Dangerous assumptions

- Do not assume `this`, `document.thisItem`, and `parent.thisItem` are interchangeable.
- Do not assume `top.aras` or `parent.aras` is a public universal API merely because a classic-client snippet works.
- Do not assume a Promise-returning Client Method is awaited by its event dispatcher.
- Do not assume a hidden button or client validation prevents direct AML/API access.
- Do not assume DOM IDs, grid objects, dialog signatures, or cache internals survive another client or hotfix.
- Do not assume a successful HTTP response means the returned Aras Item is not an Error Item.
