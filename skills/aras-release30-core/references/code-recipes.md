# Safe code recipes

These are structural templates. Replace ItemType/property names and verify signatures against the target-release IOM reference. Never paste credentials or real production GUIDs.

## Bounded C# query

```csharp
Innovator inn = this.getInnovator();

Item query = inn.newItem("Part", "get");
query.setProperty("item_number", requestedNumber); // IOM serializes the value
query.setAttribute("select", "id,item_number,name,state");
query.setAttribute("maxRecords", "2");

Item result = query.apply();
if (result.isError())
{
    return inn.newError("Unable to retrieve the Part. Reference: " + correlationId);
}

int count = result.getItemCount();
if (count == 0)
{
    return inn.newError("Part was not found.");
}
if (count > 1)
{
    return inn.newError("Part number is not unique. Reference: " + correlationId);
}

Item part = result.getItemByIndex(0);
string name = part.getProperty("name", "");
return inn.newResult(name);
```

Log the technical `result.getErrorString()`/detail in a protected, configured server sink with `correlationId`; do not return raw detail to the client.

## Explicit-ID update

```csharp
Innovator inn = this.getInnovator();

Item update = inn.newItem("Part", "edit");
update.setID(validatedPartId);
update.setProperty("description", validatedDescription);

Item result = update.apply();
if (result.isError())
{
    return inn.newError("Part update failed. Reference: " + correlationId);
}

return result;
```

Before using `edit` versus `update`, verify target-release lock and generation behavior. Never replace the explicit ID with a broad `where` just to save a loop.

## Add a relationship with a related Item

```csharp
Innovator inn = this.getInnovator();

Item source = inn.newItem("Part", "edit");
source.setID(validatedParentPartId);

Item relationship = inn.newItem("Part BOM", "add");
relationship.setProperty("quantity", validatedQuantityText);

Item related = inn.newItem("Part", "get");
related.setID(validatedChildPartId);
relationship.setRelatedItem(related);

source.addRelationship(relationship);
Item result = source.apply();

if (result.isError())
{
    return inn.newError("BOM relationship could not be added. Reference: " + correlationId);
}
return result;
```

`quantity` belongs to the `Part BOM` Relationship Item, not the child Part.

## `OnBefore*` validation

```csharp
Innovator inn = this.getInnovator();
string requiredValue = this.getProperty("required_property", "");

if (string.IsNullOrWhiteSpace(requiredValue))
{
    return inn.newError("Required property must be provided.");
}

// For a Server Event, successful completion does not return a replacement Item.
// Leave the Method without a success return statement; the context AML continues.
```

The official Server Event contract says an Event Method returns an Item only when it wants to return an error. Confirm the target-release event documentation if a specialized event differs.

## Production-safe error boundary

```csharp
Innovator inn = this.getInnovator();
string correlationId = System.Guid.NewGuid().ToString("N");

try
{
    return ExecuteBusinessOperation(inn, this, correlationId);
}
catch (System.Exception ex)
{
    // Implement this adapter with the logging facility configured for the target release.
    LogProtectedException(correlationId, ex);
    return inn.newError("The operation failed. Contact support with reference " + correlationId + ".");
}
```

Do not implement `LogProtectedException` by writing to an arbitrary web-root file. Verify sink, ACL, rotation, retention, and redaction. If the hosting contract requires rethrow, use `throw;` after logging rather than `throw new Exception(ex.ToString())`.

## Client validation plus server enforcement

Client Method logic for immediate feedback. Pass the context Item into this function from the documented binding for the target client; do not hard-code `document.thisItem`, `parent`, or frame traversal:

```javascript
function validateRequired(contextItem, arasApi) {
  if (!contextItem || !arasApi) {
    throw new Error("Unsupported Aras client binding context");
  }

  const value = contextItem.getProperty("required_property", "").trim();
  if (!value) {
    arasApi.AlertError("Required property must be provided.");
    return false;
  }
  return true;
}
```

The validation logic uses public Item behavior; obtaining `contextItem`/`arasApi` is a `Compatibility` concern because the binding differs among Form, Field, Grid, CUI, and client generations. Put that lookup in a versioned adapter. Pair it with an `OnBeforeAdd`/`OnBeforeUpdate` server validation. Then test the server directly with AML from an unauthorized or malformed request; do not accept a UI-only test.

## Query relationships without confusing object roles

```csharp
Item source = inn.newItem("Part", "get");
source.setID(validatedParentPartId);
source.setAttribute("select", "id,item_number");

Item rel = inn.newItem("Part BOM", "get");
rel.setAttribute("select", "id,quantity,related_id(item_number,name)");
source.addRelationship(rel);

Item result = source.apply();
```

Read `quantity` from each Relationship Item and child properties from its related Item. Bound the result set if the relationship can be large.

## Outbox skeleton for external integration

Within the same Aras transaction as the business change, add an `Integration Outbox` Item containing:

```text
event_type
aggregate_id
aggregate_generation
idempotency_key
payload_version
payload (sanitized/minimal)
status = Pending
attempt_count = 0
next_attempt_on
correlation_id
```

An Agent/background worker claims pending records, calls the remote service with `idempotency_key`, records success, or schedules bounded retry. Make claiming concurrency-safe and move exhausted records to a reviewable dead-letter state.

## Raw AML escape hatch

Use raw AML only when nested structure is materially clearer than IOM. Construct it with an XML API. If a legacy boundary forces text, XML-escape values and never insert raw user text into attributes, element names, `where`, or XPath. Unit-test quotes, ampersands, angle brackets, Unicode, empty values, and malicious payloads.
