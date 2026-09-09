# Modeling and development guide

## Item model

Think in four separate objects:

```text
Source Item -> Relationship Item -> Related Item
                  owns quantity, sequence, role, flags, comments, etc.
```

An ItemType defines shape and behavior. Item, ItemType, Property, Method, Identity, Lifecycle, Workflow, Form, and many configuration constructs participate in the Item model. Normal persistence maps ItemTypes to SQL tables and Properties to columns, but SQL layout is an implementation detail—not an extension API.

## AML and IOM

AML is XML expressing one or more Item actions. Common actions include `get`, `add`, `edit`, `update`, `delete`, `promoteItem`, and named Server Methods. IOM constructs and consumes this AML through `Innovator` and `Item` objects.

An IOM `Item` may represent:

- one Item;
- a collection;
- an error;
- a scalar/result wrapper;
- a logical expression.

Always test `isError()` and expected cardinality before reading properties.

### `applySQL` empty-result count

Treat `applySQL` result counting as `Compatibility` behavior and verify it on the target release. After checking `isError()`, interpret `getItemCount() <= 0` as no matching row and only a positive value as a hit. Do not test only `getItemCount() == 0`: in observed server Method runtimes, an empty `applySQL` result commonly reports `-1`, which can incorrectly skip an add-or-create branch.

```csharp
Item rows = inn.applySQL(validatedReadOnlySql);
if (rows.isError())
{
    return inn.newError("The lookup failed.");
}

if (rows.getItemCount() <= 0)
{
    // No matching row; execute the intended public IOM/AML business action.
}
```

This rule is specific to interpreting legacy `applySQL` query results. It does not make direct SQL an approved business-write path, and the error check must come first so that `-1` does not hide an Error Item.

### Safe query rules

- Set `type`/`action` explicitly.
- Prefer `id` or keyed criteria; avoid broad raw `where` expressions.
- Use `select` to retrieve only required properties.
- Use `page`/`pagesize` or `maxRecords` for large sets.
- Bound relationship expansion; use `levels` only with a justified maximum.
- Retrieve related properties explicitly, e.g. `related_id(item_number,name)`, when supported by the target release.
- Use `doGetItem="0"` only when the caller intentionally needs no returned Item and tests still verify success/affected identity.
- Do not assume ordering unless `orderBy` is explicit.

### Batch rules

An `<AML>` root may contain multiple Item actions. Batch only when atomicity, event order, lock behavior, response shape, and maximum size are understood. Build clean request Items or XML nodes; do not recycle UI-context Items carrying `isNew`/`isTemp` state and do not concatenate unescaped strings.

## Method contexts

### Client Method

- JavaScript in the browser.
- Access to context varies by binding: Item action, generic action, form/field event, relationship grid, CUI, or client ItemType event.
- Use it for presentation and interaction. Never make it the sole authorization or invariant layer.
- `this.getInnovator()` is the preferred context when available. Older `top.aras.newIOMInnovator()` and frame traversal are compatibility techniques, not stable defaults.

### Generic/Action Server Method

- C# server code receives a context Item and authenticated connection.
- Build results with `inn.newResult(...)` for scalar results or `inn.newError(...)` for safe errors.
- A Method invoked as an action should return the Item-shaped contract expected by its caller.

### Server Event Method

- `OnBefore*`: receives request AML, can validate/transform, and an error stops the action.
- `On*`: replaces normal action behavior; use sparingly.
- `OnAfter*`: receives/operates on response semantics and an error rolls back the Aras transaction.
- Do not generalize “all server Methods must return an Item” to every event. For event hooks, return an error only when failing unless the specific event contract documents replacement data.

Common ItemType events include add/update/delete/get/promote/copy/lock/unlock/version stages. Lifecycle and Workflow expose their own pre/post/activity/path events. Verify the exact event names and timing in target-release documentation.

## Lock, edit, and update

Lock semantics depend on the action and target release. Do not rely on training shorthand such as “edit always locks and unlocks automatically” as a universal rule. Decide whether optimistic update, explicit lock/edit/unlock, or another documented action fits the UI and concurrency contract. Test:

- not locked;
- locked by current user;
- locked by another user;
- stale generation/version;
- concurrent update.

## Client events and CUI

Client events (`OnBeforeNew`, `OnNew`, `OnAfterNew`, `OnShowItem`, form/field/grid events) can initialize fields, filter searches, and improve feedback. CUI composes Presentation Configuration, Window/Command Bar Sections, Controls, Item actions, Identity qualifiers, classification, and sort order.

Treat these as UX configuration:

- `Can Execute`, Identity qualification, hidden, disabled, and read-only controls do not replace Permission Items or server validation.
- Prefer CUI metadata to DOM manipulation.
- Qualify CUI behavior by target release/client type and verify in every supported browser/client.

## XPath

XPath operates on the XML DOM already returned; AML criteria operate on the server query. Use AML to limit server data, then XPath for local selection.

- Prefer absolute/anchored paths over broad `//` scans.
- Do not interpolate untrusted values into XPath.
- Assume XPath 1.0 unless target documentation proves extensions.
- Standard function spelling is `starts-with`; standard XPath 1.0 has no `ends-with`.
- Test namespace, quoting, empty collection, and multiple match behavior.

## Files and Vault

Use File Items and documented `setFileProperty`/`fetchFileProperty` or target-release Vault APIs. `fetchFileProperty` may return/download to a location according to its mode; physical Vault folder paths are not durable contracts. Validate authorization, filename handling, size, malware policy, and cleanup.

## External .NET IOM clients

Use release-matched IOM assemblies and a documented connection factory. Keep server URL, database, username, and credentials in protected configuration; never hard-code `admin`/password as shown in teaching examples. Handle login error Items, TLS validation, timeouts, session disposal, and release compatibility.

## Packaging and release

Package every custom ItemType, Property, RelationshipType, Form, Method, Lifecycle, Workflow, Permission, CUI object, and dependency. Avoid environment-specific GUIDs/URLs where a keyed name or deployment setting is appropriate. Promotion must include:

- target release/SP/hotfix;
- dependency order;
- configuration transform/secrets procedure;
- smoke and rollback tests;
- list of private/compatibility APIs and their owners.
