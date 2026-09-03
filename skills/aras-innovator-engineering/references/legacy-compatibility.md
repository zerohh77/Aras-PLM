# Legacy and private API quarantine

The internal materials target Aras 12 and contain useful clues about classic-client behavior. They are not proof of a public API in later clients.

## Compatibility/private examples

Treat these patterns as `Compatibility` or `Private` until target-release documentation proves otherwise:

- `top.aras.newIOMInnovator()` when a documented context Innovator is available.
- `parent.document.getElementById("instance").contentDocument.thisItem`.
- `document.thisItem`, `parent.thisItem`, and frame/window traversal whose availability depends on binding.
- `top.aras.uiShowItemEx(...)`, `uiReShowItemEx(...)`, `itemsCache` manipulation.
- `parent.relationships.iframesCollection[...]` and hard-coded iframe IDs.
- `grid.items_Experimental`, `gridApplet.Cells(...)`, `topWnd.main.work.grid`.
- Direct DOM style changes to Aras-owned controls instead of CUI/Form APIs.
- Hard-coded control IDs, generated GUIDs, or CSS classes.
- Older permission-elevation helpers, MD5 helpers, and authentication snippets.

## Adapter rule

Put each unavoidable private interaction behind one named adapter:

```javascript
// arasClassicAdapter.js — the only module allowed to touch classic grid internals.
function getSelectedItemIds(context) {
  if (!context || !context.grid) {
    throw new Error("Unsupported Aras client context");
  }
  return context.grid.getSelectedItemIds(";"); // verify exact release signature
}
```

The actual adapter must:

- check target release/client at startup;
- feature-detect objects/methods;
- fail closed with a clear compatibility error;
- expose a small product-owned interface;
- have UI regression tests in every supported client/browser;
- be listed in package/release notes with owner and removal plan.

Do not copy the illustrative call above until verified on the target release.

## Reject list from teaching examples

- Hard-coded `admin` credentials in external .NET code.
- `ScalcMD5` as a modern authentication design.
- `throw new Exception(ex.ToString())` for user-visible diagnostics.
- Full `getErrorDetail()`/stack trace shown to users.
- `applySQL("select * ...")` as normal application logic.
- Direct SQL business writes under elevated Identity.
- Concatenated AML/XML with unescaped values.
- `serverEvents="0"` as routine performance tuning.
- CUI/field hiding described as security enforcement.
- Physical Vault path as a durable application path.

## Version migration checklist

1. Inventory all client Methods containing `top`, `parent`, `iframe`, `contentDocument`, `grid`, `Applet`, `itemsCache`, `style`, or hard-coded GUIDs.
2. Classify each as public, compatibility, private, or dead.
3. Replace with CUI/Form/public APIs where available.
4. Consolidate remaining private calls in adapters.
5. Test item window, tear-off, search grid, relationship grid, new/edit/read-only states, and supported browsers.
6. Remove code that silently assumes a frame exists.
