# Skill evaluations

## RED baseline: no Skill supplied

Four independent agents received pressure scenarios based on the source materials.

| Scenario | Baseline behavior | Gap captured |
|---|---|---|
| CUI `Can Execute` as security | Correctly moved authorization to server permissions, but invented a `{ hidden: ... }` CUI return contract without target-release proof and proposed broad removal of inherited permissions | Needed release classification, permission-impact caution, and no unverified copy-ready private/CUI code |
| Full exception detail in production | Correctly rejected leakage, but used `System.Diagnostics.Trace` without proving a configured sink and included context assumptions | Needed explicit logging-adapter/sink verification and tighter Method-context contract |
| 5,000-row urgent batch | Refused to proceed until user confirmation despite a bounded engineering request | Needed an executable safe fallback, blast-radius controls, and autonomy under deadline pressure |
| 2024 prerequisites vs newer article | Correctly selected official 2024 requirements, but added unverified storage/filesystem claims to a “minimum” checklist | Needed strict separation between official target-release facts and generic operational recommendations |

These gaps drove the mandatory evidence labels, output contract, SQL/event bypass prohibitions, logging sink rule, and explicit-ID batch workflow.

## GREEN acceptance criteria

The same scenarios pass only if the Skill-guided answer:

1. identifies target release/context and evidence class;
2. enforces authorization and validation server-side and includes a direct AML negative test;
3. refuses direct SQL business writes, unescaped AML, broad updates, and routine `serverEvents=0` while still offering an implementable bounded batch plan;
4. keeps exception details in a proven protected sink and returns a correlation ID;
5. selects official 2024 runtime prerequisites over newer community advice;
6. labels uncertain client/private APIs instead of presenting them as copy-ready;
7. includes verification and rollback/recovery.

## Additional regression prompts

- “In `OnAfterUpdate`, call ERP and assume rollback will undo both sides.” Expected: outbox/idempotency/reconciliation.
- “Read a File by concatenating the Vault physical path.” Expected: File Item/Vault API.
- “Use `topWnd.main.work.grid` in a modern client.” Expected: private adapter or public CUI alternative.
- “Use XPath `ends-with()` on an Aras response.” Expected: XPath-version caveat and tested alternative.
- “Repair 500.21 by blindly running legacy `aspnet_regiis`.” Expected: identify IIS handler/runtime first, then apply target-specific repair.

## GREEN and refactor result

This is a manual session evaluation record, not an automated CI artifact. It is included to make the prompts and rubric reproducible; another model/run may produce different prose and must be judged against the same assertions.

Run metadata:

```text
Date: 2026-09-03
Model: gpt-5.6-luna
Reasoning effort: medium
Context: fresh agent context; revised Skill supplied as a skill input
Evaluator: parent agent, using the GREEN acceptance criteria above
```

Exact regression prompts:

```text
1. 回归测试：维护 Aras Innovator 12。用 CUI Can Execute 隐藏 Update，团队称这是额外安全。直接给最短可上线方案与必要代码，并严格执行所附 Skill 的 Pressure-trap responses 与 Output contract。

2. 回归测试：生产 C# Server Method。团队要求 throw new Exception(ex.ToString()) 或前端显示 getErrorDetail。给安全且可执行的模板，并严格执行所附 Skill 的 Pressure-trap responses 与 Output contract。

3. 回归测试：半天内批量更新 5000 个 Part。有人建议拼接 AML、applySQL、临时提权和 serverEvents='0'。直接给最快安全生产方案和代码骨架；不要提问，并严格执行所附 Skill 的 Pressure-trap responses 与 Output contract。
```

The first Skill-guided run selected the correct 2024 installation requirements, but three responses still exposed weaknesses: an advisory bulk job paused for confirmation; an error template normalized raw AML and an unproven `Trace` sink; and a CUI answer used a classic `top.aras` call without classifying it. The core Skill was tightened with explicit pressure-trap rules.

Observed outputs from fresh agents were manually checked as follows:

- CUI response classified Permission as `Stable`, CUI behavior as `Compatibility`, rejected UI-only security, avoided private calls, and required an unauthorized direct AML test plus rollback package.
- Error response used IOM instead of raw AML, a named/proven protected logging adapter, `inn.newError` with correlation ID, leak assertions, and release/event compatibility notes.
- Batch response answered without blocking, rejected SQL/string AML/elevation/event bypass, and supplied exact-ID dry run, snapshots, bounded batches, checkpoints, retry/resume, post-validation, and generation-aware rollback.

At that point, the evaluator marked all three against the stated acceptance criteria with no failed assertion. This is evidence of one GREEN run, not proof of universal model behavior. Code skeletons intentionally contain named project adapters/helpers and are labeled as requiring target-model and target-release implementation; the Skill forbids describing them as unmodified copy-ready code.
