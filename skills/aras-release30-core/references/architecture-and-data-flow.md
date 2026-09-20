# Architecture, data flow, and design philosophy

## Core model

Aras Innovator is a metadata-driven transactional platform. “Everything is an Item” means business records and much of the schema/configuration are represented as Items. An ItemType describes data shape and behavior; a normal ItemType maps to a database table and its Properties map to columns. Relationships are also Items:

- `source_id`: source Item
- Relationship Item: owns relationship-specific properties such as quantity, sequence, or role
- `related_id`: related Item, if the relationship has one

Never place relationship data on the related Item merely because it is shown in the same grid.

## Primary request data flow

```text
User / external .NET client
  -> browser Client Method/CUI or IOM connection
  -> HTTP(S), SOAP/XML; public request expressed as AML Item actions
  -> IIS reverse proxy in standard MSI deployment
  -> Innovator Server on .NET/Kestrel
       -> OAuth authentication/discovery
       -> Identity/Permission evaluation
       -> Item action dispatcher
       -> OnBefore* validation/transform
       -> standard action or On* replacement
       -> SQL transaction and Item persistence
       -> OnAfter* response processing
       -> AML result: single Item / collection / error / result / logical
  -> client renders result or external client consumes it
```

IOM is an object model over AML; it does not create a second security or persistence path. Public IOM/AML requests still pass through server permissions and event logic unless deliberately bypassed by dangerous options.

## File and background flows

```text
Client -> Innovator Server -> File Item metadata -> Vault Server -> protected file storage
                                      |
                                      +-> Agent Service -> replication / scheduled background work
                                      +-> Conversion Server -> conversion tasks and generated artifacts
```

Vault is managed through Innovator and Vault APIs; its physical storage is not a public application interface. Agent is required for Vault replication or Conversion work. Conversion is resource intensive and is normally isolated from the main Innovator host.

## Authentication and configuration flow

```text
Client/Server/Agent -> OAuth discovery URL -> token/authentication services
Innovator Server    -> InnovatorServerConfig.xml -> database/mail/runtime settings
Vault/Agent/OAuth   -> component-specific configuration, certificates, URLs, ports
```

Every URL must be resolvable from the component that consumes it. `localhost` is valid only when consumer and service are on the same host. Certificates, DNS, reverse-proxy bindings, and discovery documents form one chain.

## Module dependencies

```text
Client UI/CUI
  depends on -> Innovator Server public endpoints

Innovator Server
  depends on -> IIS/reverse proxy, .NET runtimes, OAuth, SQL database, license
  coordinates -> permissions, lifecycle/workflow, Methods/Events, mail
  references -> Vault endpoints

Vault Server
  depends on -> Innovator Server URL, storage, TLS/DNS

Agent Service
  depends on -> Innovator/OAuth reachability, unique alias, free port, service identity
  enables -> Vault replication and Conversion orchestration

Conversion Server
  depends on -> Agent/service configuration, VC++ runtime, capacity

SQL database
  depends on -> supported SQL release, SQL authentication, owner + regular accounts
  must match -> Innovator code-tree release/hotfix
```

## Design philosophy

- **Metadata/configuration first.** ItemTypes, Properties, Relationships, Forms, Lifecycles, Workflows, Permissions, and CUI are first-class extension points.
- **Public protocol beneath object APIs.** AML is the request/response language; IOM is the safer object façade.
- **Server is authoritative.** Browser behavior improves usability; permissions, invariants, transactions, and audit belong on the server.
- **Event-oriented extension.** `OnBefore`, `On`, and `OnAfter` hooks intercept Item actions with different semantics.
- **Plugin-like composition with release-sensitive UI seams.** Configuration and public Item operations are durable; browser frames, grids, DOM, and undocumented methods are fragile.
- **Explicit operational topology.** Database, Vault, OAuth, Agent, Conversion, certificates, and configuration are separately deployable yet operationally coupled.
- **Convention plus configuration, not convention alone.** Naming and Item patterns matter, but behavior is largely metadata-configured and must be packaged/versioned.

## Architectural smell test

Redesign when any answer is “yes”:

- Can a client-side check be bypassed by posting AML directly?
- Does code depend on a frame name, hard-coded DOM ID, grid internals, or a physical Vault path?
- Does a business write avoid Item actions or Server Events?
- Can retry duplicate an email, ERP mutation, or generated file?
- Is a query unbounded or does it return properties the consumer never uses?
- Can an update target more Items than intended without checking affected IDs/count?
- Would restoring only SQL leave Vault/configuration/certificates inconsistent?
