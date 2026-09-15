# Aras Innovator 2024 installation runbook

This reference is specific to **Aras Innovator 2024 Release**. Do not transplant requirements from newer releases.

## Preflight

Record these before changing a server:

- Installation type: new install, repair, or separately planned upgrade/migration.
- Topology: Innovator Server, Web/IIS, Vault, SQL, OAuth, Agent, Conversion hosts.
- DNS names and externally consumed URLs; no underscores in the Innovator hostname.
- Trusted TLS certificate chain and private-key ownership for each service.
- Service accounts, port allocation, firewall path, proxy/load-balancer path.
- SQL instance/version, SQL Authentication status, owner and regular login names.
- Server MAC address and matching Framework License Key.
- Vault path, capacity, access control, backup, and restore plan.
- Exact installer media and checksum; retain the original MSI.

## Official prerequisites

- Client: supported Windows 10/11 or macOS environment per guide.
- Server OS: Windows Server 2012, 2012 R2, 2016, 2019, or 2022.
- IIS: 8 or 10 with required roles/modules.
- .NET Framework 4.7.2.
- ASP.NET Core/.NET Runtime and Hosting Bundle 6.0.6, including AspNetCoreModuleV2.
- Microsoft Visual C++ redistributables 2015/2017/2019.
- SQL Server 2012 through 2022 with SQL Server Authentication enabled.
- Memory: 16 GB minimum, 32 GB recommended.
- Administrative rights to install; prepare SQL administrative credentials for provisioning, not runtime use.

Install/enable IIS before repairing or installing ASP.NET components so IIS modules are registered correctly. Reboot or repair components when the installer/runtime requires it.

## Installer semantics

- The installer does **not** upgrade an older code tree or database.
- Database release and code-tree release must match.
- `Complete` installs all features and generates the OAuth password rather than presenting the custom password screen.
- `Custom` defaults include Innovator Server, Vault, Database, and OAuth; Conversion and Agent are not default selections.
- Installer database modes include Create, Populate, Use Existing, and Configure-only/development scenarios. Confirm the mode before proceeding.
- A rerun can behave as a new install. If Windows Installer metadata is unavailable and a different MSI only offers Modify/Repair, the guide provides `ChangeGUID.exe`; use it administratively and preserve evidence.
- Full uninstall removes the server. Back up and verify restore before uninstalling anything material.

## Security and identity

- Create two SQL logins:
  - owner/elevated account conventionally named `innovator`, owner of non-system objects;
  - limited runtime account conventionally named `innovator_regular`.
- Do not run the application as `sa`.
- Default Innovator administrative login is `admin` / `innovator`; change or disable it before production.
- OAuth is required. OAuth passwords cannot contain spaces.
- A separate OAuth host must publish an externally resolvable hostname, not `localhost`; distribute the required certificate chain to consuming hosts.
- Use a certificate trusted by clients and servers. A self-signed certificate can prevent client/server login.

## Component rules

- Every new instance needs one Vault named `Default`.
- Vault is not standalone; configure its Innovator Server URL and protect storage from deletion by unrelated processes/users.
- Agent is required for Vault Replication or Conversion. Give each Agent a unique alias and a free port.
- Conversion Server is normally separate from Innovator Server; co-location can significantly reduce performance. Install the required VC++ runtime.
- For Agent HTTPS/Kestrel, configure the certificate correctly and encrypt stored certificate passwords using the documented `RsaCrypt` process.
- SMTP defaults to `queue`; configure a valid SMTP or Microsoft Graph mail provider. For Graph, define one Mail node; if multiple exist only the first is used, and the app requires `Mail.Send`.

## Post-install configuration

1. Confirm `InnovatorServerConfig.xml` database connections and mail settings.
2. Set `CorporateTimeZone` before production use. A later change requires all users to log out and the WWW service to restart.
3. Restart IIS after changing server configuration.
4. Disable `DebugServerMethod` in production unless explicitly needed; it creates unsigned runtime DLLs under `Server/dll` and can be disabled without negative production effect.
5. Verify feature licenses before enabling Vault replication, alternative authentication, Batch Loader, CAD-to-PDF, or add-ons.

## Acceptance matrix

| Check | Pass condition |
|---|---|
| URL/TLS | Trusted chain; no certificate warning; hostname has no underscore |
| OAuth | Discovery endpoint reachable from client, server, Vault/Agent as applicable |
| Login | Normal identity succeeds; bad credentials fail safely |
| SQL | Server uses limited runtime login; owner login reserved for administration |
| CRUD | Authorized add/edit/delete succeeds; unauthorized direct AML fails |
| Vault | Upload, download, permission denial, capacity path all verified |
| Mail | Test notification reaches intended sink without exposing secrets |
| Agent | Service starts, alias/port unique, job produces observable result |
| Conversion | Runs on intended host and does not starve Innovator workload |
| Recovery | Coordinated restore test covers DB, Vault, configuration, certs/keys |

## Known installation symptom map

- `500.21`: official guide associates with ASP.NET/IIS registration order; verify IIS features and repair/register the required runtime components for the actual .NET stack.
- `401` after login: verify IIS Windows Authentication role; repair/reinstall if necessary.
- `404` on tear-off windows: IIS extensionless URL handling missing/misconfigured.
- Grid has no columns or XML “Incorrect comments” error: wrong XML parser/component.
- Cookie error: hostname contains underscore or another invalid/non-alphanumeric pattern.
- `500` mentioning `AspNetCoreModuleV2`: Hosting Bundle/module missing or broken.
- Redirect loop: IIS HTTP Redirect module missing or configuration inconsistent.
- OAuth discovery access error: discovery URL/password/certificate/hostname is wrong.

The `500.21` remedy in the guide references legacy ASP.NET registration. Treat that command as an official troubleshooting clue, but first confirm the failing IIS handler/runtime so a legacy fix is not applied blindly to the .NET 6 reverse-proxy path.
