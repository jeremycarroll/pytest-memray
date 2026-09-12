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

## R2 delivery fan-out — 2026-09-12

[100-108](https://linear.app/1000lines/issue/100-108) applied the
[accepted R2 plan](https://github.com/jeremycarroll/pytest-memray/blob/4ad23afc66c5a82ed959cd939e7b4e06af1f67d6/docs/symphony-plans/fan-out-plan-100-102-full-captures.md)
and its [execution contract](https://github.com/jeremycarroll/pytest-memray/blob/4ad23afc66c5a82ed959cd939e7b4e06af1f67d6/docs/symphony-plans/full-captures-execution-contract.md).
Jeremy approved [PR #8, review 5187789026](https://github.com/jeremycarroll/pytest-memray/pull/8#pullrequestreview-5187789026)
at 2026-09-12 19:54:01 UTC on `4ad23afc66c5a82ed959cd939e7b4e06af1f67d6`,
then merged it at 19:54:17 UTC as `2acb32b6b1afa4c17770263e103c73dc893f84f9`.
100-107 is Done. The original d403161 commissioning and creation evidence above
remains historical; R2 alone authorizes the two additional delivery nodes.

### New issue and branch mapping

| Node | Payload key | Created issue                                                                                                               | Linear UUID                            | Branch at dispatch                                    |
| ---- | ----------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ----------------------------------------------------- |
| FC_D | FC-D        | [100-113](https://linear.app/1000lines/issue/100-113/publish-and-review-the-clean-full-captures-contribution-branch)        | `1a45fc49-dc51-42e0-b4c8-bd75f4920407` | `symphony/full-captures/100-113/prepare-clean-branch` |
| FC_E | FC-E        | [100-114](https://linear.app/1000lines/issue/100-114/certify-and-submit-the-accepted-clean-branch-upstream-with-the-actual) | `f08ac95f-3810-4541-981a-8299274c4bc1` | `symphony/full-captures/100-114/submit-upstream`      |

The complete project issue set was read before creation: no prior FC-D/FC-E
ticket existed. Only these two issues were created. FC-A/100-104, FC-B/100-105,
FC-C/100-106 and completed seeds retain their identities, descriptions, labels
and Done state. Existing unrelated relations were preserved.

Both new issues were staged in **Backlog** with project
`13af5f34-7e77-4b32-863f-97ded4ea9b16`, Jeremy assignment
`c65b9fbe-e740-47e9-b444-3172d3526ff2` and orange label
`828cfcc1-d75d-45b3-82ed-dbdc964147ff`. Full body, metadata and direct relation
readbacks passed before activation; both final readbacks are **Active**, without
mature. This is the fan-out checkpoint, not implementation completion.

The branch templates remain `symphony/full-captures/${issue}/prepare-clean-branch`
and `symphony/full-captures/${issue}/submit-upstream`. Both task branches start
from current **main** at dispatch; both task PRs target **main**, start draft,
require orange/symphony labels and are assigned to jeremycarroll. This fan-out
created neither delivery task branch nor delivery task PR. Workers must not
commit unmerged annotation work into their branches.

### Verified new direct relations

| Blocker (`issueId`)                                   | Blocked (`relatedIssueId`)                            | Relation UUID                          |
| ----------------------------------------------------- | ----------------------------------------------------- | -------------------------------------- |
| [100-106](https://linear.app/1000lines/issue/100-106) | [100-113](https://linear.app/1000lines/issue/100-113) | `98997ae8-d20c-4774-ac97-75f2c3083c5e` |
| [100-113](https://linear.app/1000lines/issue/100-113) | [100-114](https://linear.app/1000lines/issue/100-114) | `8422f28a-6fda-4cd1-8c97-caaed581ee38` |

```json
[
  {
    "issueId": "ca9ab374-b3fe-4f6d-b186-1cb5ef6c4e11",
    "relatedIssueId": "1a45fc49-dc51-42e0-b4c8-bd75f4920407",
    "type": "blocks"
  },
  {
    "issueId": "1a45fc49-dc51-42e0-b4c8-bd75f4920407",
    "relatedIssueId": "f08ac95f-3810-4541-981a-8299274c4bc1",
    "type": "blocks"
  }
]
```

Both directions of all four implementation edges were read back, exactly once.
The existing A/B→C relation IDs above were reused; only C→D and D→E were added.
The seed chain 100-106→100-107→100-108 remains separate. Automatic related links
from 100-108 to the new tickets are non-blocking; no extra runtime edges or
transitive blockers were inferred. FC-E waits for accepted FC-D, Done and its
preparation record merged to main despite its Active state.

### Body fidelity and artifact ownership

The complete [100-113 body](https://linear.app/1000lines/issue/100-113) and
[100-114 body](https://linear.app/1000lines/issue/100-114) begin with their exact
accepted summaries, creates/edits/exclusions, acceptance checks and validation
commands; FC-D's empty edits remain `none`. They include scope, file/external
ownership, required actions, delivery notes, dependencies, pinned source links,
decisions, shared execution/validation obligations and executable recipes.
FC-E identifies the clean-branch record as a future accepted FC-D output instead
of linking a nonexistent file in the accepted plan snapshot.

Unchanged shared DAG helpers validated the five-node/four-edge graph, manifest,
branch table and relation table/JSON, and previewed only FC-D/FC-E. The core
renderer omits node content; the accepted fields and contract were transcribed
into complete structured inputs before writes. After identifiers were returned,
descriptions were replaced in place with resolved links/branches. Independent
Markdown token comparison verified the entire saved content, links and code;
Linear's cosmetic wrapping/list normalization did not change the payload.

| Complete saved body at staging | SHA-256                                                            |
| ------------------------------ | ------------------------------------------------------------------ |
| 100-113                        | `24ad17f69976aa75f8812bdaa63bc34bef9678dad783586c78df024905906d43` |
| 100-114                        | `fa0e96949a92fed6396cffc12a56119e365c805908511b003ccf6e4a2bb4fc5e` |

FC-D owns the separate fork artifact `refs/heads/full-captures-upstream` and
`docs/symphony-plans/full-captures-clean-branch.md`. FC-E receives branch writes
only after Jeremy accepts the frozen artifact and FC-D is Done with its record
merged. FC-E owns the actual upstream PR, genuine DCO/access verification,
submission record and exact observed-number news rename on both surfaces.
Jeremy remains the resource owner and human acceptance owner. No artifact,
certification or upstream submission was performed by this seed.

Both graph copies now label FC_D as 100-113 and FC_E as 100-114. Node IDs,
payload keys, branch templates, relation payloads and endpoints remain unchanged.
Clicks remain omitted because the supported shared parser rejects them; the
tables provide the actual issue links. Detailed mutation inputs, complete API
snapshots, validation and next owner are recorded in the pinned
[100-108 Codex Workpad](https://linear.app/1000lines/issue/100-108).
