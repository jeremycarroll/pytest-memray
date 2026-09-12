# Full-captures fan-out record

[100-103](https://linear.app/1000lines/issue/100-103) created the three tasks below from the [accepted plan](https://github.com/jeremycarroll/pytest-memray/blob/d403161792521f57d9a633c09b99c9d07fd5c1a2/docs/symphony-plans/fan-out-plan-100-102-full-captures.md) and its [execution contract](https://github.com/jeremycarroll/pytest-memray/blob/d403161792521f57d9a633c09b99c9d07fd5c1a2/docs/symphony-plans/full-captures-execution-contract.md).
Jeremy Carroll approved plan PR #3 at 2026-09-12 17:29:11 UTC on `d403161792521f57d9a633c09b99c9d07fd5c1a2` and merged it to main as `874241401eb4016be2d1179785b58f17d997c829`.
The plan's historical proposal text describes that review stage; human approval and merge establish the accepted baseline.

## Issue and branch mapping

| Node | Payload key | Created issue                                                                                                               | Branch at dispatch                                      |
| ---- | ----------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| FC_A | FC-A        | [100-104](https://linear.app/1000lines/issue/100-104/add-full-capture-selection-with-configuration-and-reporter-regression) | `symphony/full-captures/100-104/full-capture-selection` |
| FC_B | FC-B        | [100-105](https://linear.app/1000lines/issue/100-105/document-full-capture-configuration-and-downstream-reporter-use)       | `symphony/full-captures/100-105/full-capture-docs`      |
| FC_C | FC-C        | [100-106](https://linear.app/1000lines/issue/100-106/validate-the-combined-change-and-finalize-upstream-submission-or)      | `symphony/full-captures/100-106/finalize-full-captures` |

Every branch is created at dispatch from current `main`; every task PR targets `main` and starts draft. This record declares branches; fan-out did not create implementation branches or PRs.
All issues were created in **Backlog**, verified with complete bodies and both direct blocker directions, then moved to **Active**.
The issue/API readback is the creation checkpoint, not a claim of implementation or completion.
All are assigned to Jeremy Carroll and labeled `orange`; their PRs require `orange` and `symphony`.
No existing implementation/finalizer issue needed updating.

| Payload key | Linear UUID                            |
| ----------- | -------------------------------------- |
| FC-A        | `8529b5a2-af58-41d7-b1c3-0995a14160bf` |
| FC-B        | `cb829111-50a2-4d20-9622-7feece1a60ca` |
| FC-C        | `ca9ab374-b3fe-4f6d-b186-1cb5ef6c4e11` |

## Verified direct relations

`issueId` is the blocker, `relatedIssueId` is the blocked issue and `type` is `blocks`.

| Blocker                                                                                                                     | Blocked issue                                                                                                          | Relation UUID                          |
| --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| [100-104](https://linear.app/1000lines/issue/100-104/add-full-capture-selection-with-configuration-and-reporter-regression) | [100-106](https://linear.app/1000lines/issue/100-106/validate-the-combined-change-and-finalize-upstream-submission-or) | `1e51305a-ef2b-4129-9258-2fae9b0ec65a` |
| [100-105](https://linear.app/1000lines/issue/100-105/document-full-capture-configuration-and-downstream-reporter-use)       | [100-106](https://linear.app/1000lines/issue/100-106/validate-the-combined-change-and-finalize-upstream-submission-or) | `ef294ad1-6942-4442-af92-e35b9b3067fd` |

```json
[
  {
    "issueId": "8529b5a2-af58-41d7-b1c3-0995a14160bf",
    "relatedIssueId": "ca9ab374-b3fe-4f6d-b186-1cb5ef6c4e11",
    "type": "blocks"
  },
  {
    "issueId": "cb829111-50a2-4d20-9622-7feece1a60ca",
    "relatedIssueId": "ca9ab374-b3fe-4f6d-b186-1cb5ef6c4e11",
    "type": "blocks"
  }
]
```

Both outgoing and incoming relation queries matched these two payloads before activation.
No FC-A → FC-B blocker was created: its documentation coordination remains soft sequencing.
Existing seed relations 100-101 → 100-102 → 100-103 were preserved.
FC-C waits for both accepted task results to land on main; Active does not bypass those blockers.

## Content and graph proof

- Each live ticket starts with its own accepted summary and preserves creates, edits, exclusions, acceptance checks and validation commands. Empty lists remain `none`.
- All node scope, required actions, ownership, dependencies, delivery/finalization responsibilities and branch/PR policies are inline, followed by accepted decisions and the shared execution/validation sections.
- The [100-104 body](https://linear.app/1000lines/issue/100-104/add-full-capture-selection-with-configuration-and-reporter-regression) is a complete live payload example. Each source-document link pins the reviewed plan SHA. FC-C identifies the news fragment as a future FC-B output, rather than claiming it exists in that snapshot.
- Structured `issueCreate` inputs contained teamId, projectId, title, description, Backlog stateId, orange labelIds and Jeremy assigneeId. Subsequent `issueUpdate` replaced descriptions with mapped links and resolved branch names, then set Active only after readback.
- Independent API readback verified every required node field and executable command, issue identifiers/URLs, assignment, labels, staging and final states. Linear normalizes Markdown bullets, link brackets and table spacing. Executable commands use inline code so `__version__` remains literal.
- Description regeneration replaces the complete generated body; it never appends a second block. The issue-local payload evidence and field comparison found one copy of each required section.
- Unchanged shared DAG exports verified three nodes/two edges, embedded/standalone/manifest agreement and relation table/JSON/derived endpoint agreement. The shared metadata renderer was used for core payloads, with exact accepted fields transcribed into structured inputs as instructed by the accepted contract.
- Both [plan graph](./fan-out-plan-100-102-full-captures.md#dag) and [standalone graph](./fan-out-plan-100-102-full-captures.mmd) carry the mapped identifiers. Reapplying annotation replaces the identifier prefix and is idempotent. Node IDs, payload keys, manifest, branch templates and edge endpoints are unchanged.
- Mermaid clicks are omitted under the accepted execution contract because the shared parser rejects click directives. The issue mapping and relation tables above provide clickable links.

Full mutation inputs, returned IDs, readbacks, source/identity/label/state evidence and validation results are recorded in the pinned [100-103 Codex workpad](https://linear.app/1000lines/issue/100-103).
Fan-out performed no spawned implementation, package release or upstream submission.
Human acceptance owns Done.
