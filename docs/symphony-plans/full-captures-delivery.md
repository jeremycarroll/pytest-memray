# Full-capture delivery record

Preparation checkpoint for [100-106][finalizer], implementing the accepted
[plan][plan] and [design][design]. Combined acceptance and the upstream submission
package remain pending the accepted documentation result.

## Accepted inputs and resumption

The task branch starts from `jeremycarroll/pytest-memray` **main** at
`c09c1c2e56e48cecb5cec0f191c36c02f5f87341`. Its PR also targets main.

| Input                            | Observed result on 2026-09-12                                                                                                                                                                          | Finalization consequence                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| [FC-A / 100-104][implementation] | Done; [PR #6][pr-a] accepted by Jeremy and merged at 18:06:03 UTC as `c09c1c2e56e48cecb5cec0f191c36c02f5f87341`; implementation head `7d6e9d23a0ba9d4dd0149a00318e3e0405ef4df9` is an ancestor of main | Accepted implementation available                              |
| [FC-B / 100-105][documentation]  | [PR #5][pr-b] remains open at `bacc18945d555b1d8c40e08d5632330888eb364e`; its refreshed guides include the accepted implementation, but acceptance and merge remain outstanding                        | Combined docs/runtime validation and correction ownership wait |

Resume when FC-B is Done and its accepted result is merged into main. Jeremy
owns human acceptance; FC-B owns its remaining review closure. FC-C then fetches
main, records the accepted documentation commit and combined SHA, verifies both
results are ancestors, and refreshes this branch from main. No predecessor work
absent from main is included in this preparation checkpoint.

## Evidence ledger

The [FC-A workpad][proof-a] retains local execution at implementation head
`7d6e9d23a0ba9d4dd0149a00318e3e0405ef4df9`: Python 3.9.25, pytest 8.4.2,
normal Memray 1.20.0 and minimum Memray 1.19.1. Both versions produced full
captures whose stats reported 21 allocations and 82.460 kB total/peak; the
corresponding aggregated captures were rejected. Supported object tracking
passed all 12 tests with Python 3.13.15 and Memray 1.19.1 in its recorded container.
These are predecessor results, not FC-C combined-run evidence.

| Obligation                                                 | Evidence available                                                            | Remaining FC-C work                                                                                                                           |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| AC1–AC3: configuration, invalid inputs, activation/tracing | Accepted FC-A tests and [Cadence approval][review-a]                          | Verify on combined main                                                                                                                       |
| AC4–AC5: persistence and stats                             | FC-A real capture paths, commands and outputs in its workpad                  | Repeat documented command with both tracing flags, then aggregated mode, in fresh directories; record installed revision and exact output     |
| AC6 / E1: compatibility and regressions                    | FC-A normal/minimum-version and supported object-tracking proof               | Audit retained coverage, run combined regression checks and rerun demonstrated gaps only                                                      |
| AC7: documentation/news                                    | FC-B prepared guides and [runtime example evidence][proof-b]                  | Verify accepted documentation on main and build it with the implementation                                                                    |
| AC8 / E3: final fork review                                | Current fork prerequisites are identified above                               | Publish final delivery evidence; require all 12 current-head Run/Build checks, fresh hackcadence/Codex approval, closed feedback and ready PR |
| E2: actual reporter artifacts                              | Predecessor evidence is linked                                                | Record FC-C fixture, discovered binary paths, versions, commands and output                                                                   |
| E4: contribution identifiers                               | Fork PR #6 and #5 are observed; issue #160 is the provisional news identifier | Record final fork PR and actual upstream PR, or exact rename action in the completed handoff                                                  |
| E5: fork publication access                                | Author App binding succeeded for the fork                                     | Verify final branch/PR publication, orange/symphony labels and Jeremy assignee                                                                |
| E6: submission and signoff                                 | Current upstream contribution rules read; runtime upstream binding denied     | Complete product-only package after accepted combined validation; Jeremy supplies real signoff and performs authorized submission             |

Configured/effective validation mode is **native/native**, without a ticket
Docker override. Combined checks remain unrun at this checkpoint: `make check`,
`make lint`, `make docs`, distribution build, Markdown/news validation and the
full-versus-aggregated reporter workflow. Publication checks for this independent
record are tracked separately in the [FC-C workpad][proof-c]. Passing checks on
this preparation record cannot establish final project acceptance.

## Cleanup boundary

Cleanup commits: none. The combined project audit is pending FC-B acceptance.
Audit the files changed by both accepted predecessor PRs, as well as this record;
the finalizer diff alone cannot reveal remnants already merged into main.
Resolve project-introduced temporary markers and missed obligations, preserving
unrelated pre-existing markers and historical planning evidence. No temporary
integration seam is planned. The positive full-capture option is durable product
configuration, not a temporary rollout flag.

## Upstream submission preparation

The destination is `bloomberg/pytest-memray`, default branch **main**. Its observed
main SHA on 2026-09-12 is `92a9c85ccbeba900fd52d59395aae0443a0b13a7`; refresh and
record the actual base before preparing the final contribution.

The upstream package must contain only the accepted product patches for
`src/pytest_memray/plugin.py`, `tests/test_pytest_memray.py`,
`tests/test_object_tracking.py`, `README.md`, `docs/configuration.rst` and the
owned feature fragment, plus any demonstrated FC-C corrections. Extract changes
from the accepted task commits, excluding unrelated fork divergence and all
Symphony onboarding/planning files. Do not submit fork main wholesale. The exact
accepted patch, application check, commit list, title/body and final tested ref
remain FC-C deliverables after FC-B merges.

Upstream access preflight using the existing author App returned **HTTP 404**
(repository unavailable to that binding). No upstream credential or submission
permission was obtained. Fork App access does not establish upstream authority.
Jeremy owns submission through his authorized GitHub account; no App grant
expansion or alternate runtime identity is assumed.

The current [upstream contribution instructions][contributing] require a real-name
signoff on every contributed commit under its [DCO][dco]. The FC-A source commit
is App-authored and has no human signoff. Jeremy must review the final patch,
confirm his right to contribute it, and create the real signed-off contribution
commit(s). A fork approval or merge is not that certification.

After submission, read back the actual upstream PR URL, number, base, head,
diff, commit signoffs and required check results. Only then resolve and perform
the owned rename from `docs/news/160.feature.rst` to
`docs/news/<observed-upstream-PR-number>.feature.rst`, preserving the feature text
and recording the resulting commit/checks. If no upstream PR exists at handoff,
Jeremy owns that exact rename after obtaining its number. No number is invented.

The [upstream issue][upstream-issue] remains open at this checkpoint. Its four
comments, [aggregation PR #107][aggregation-pr], [release 1.6.0][release] and
official [stats][stats] / [flame graph][flamegraph] documentation were read.
No maintainer decision on this contribution has been observed. Deployment,
package publication, upstream merge and issue closure are outside this project.
Jeremy owns final project acceptance.

[finalizer]: https://linear.app/1000lines/issue/100-106
[implementation]: https://linear.app/1000lines/issue/100-104
[documentation]: https://linear.app/1000lines/issue/100-105
[plan]: https://github.com/jeremycarroll/pytest-memray/blob/d403161792521f57d9a633c09b99c9d07fd5c1a2/docs/symphony-plans/fan-out-plan-100-102-full-captures.md
[design]: https://github.com/jeremycarroll/pytest-memray/blob/d403161792521f57d9a633c09b99c9d07fd5c1a2/docs/symphony-plans/full-captures-requirements-design.md
[pr-a]: https://github.com/jeremycarroll/pytest-memray/pull/6
[pr-b]: https://github.com/jeremycarroll/pytest-memray/pull/5
[proof-a]: https://linear.app/1000lines/issue/100-104#comment-3851c547-6549-421e-bb66-61c74214d36b
[proof-b]: https://linear.app/1000lines/issue/100-105#comment-e09a7ba3-b103-4049-bca8-8e619958ba3c
[proof-c]: https://linear.app/1000lines/issue/100-106#comment-cbac84b4-303c-4e39-a9e3-369eeaaebe39
[review-a]: https://github.com/jeremycarroll/pytest-memray/pull/6#pullrequestreview-5187399243
[contributing]: https://github.com/bloomberg/pytest-memray/blob/92a9c85ccbeba900fd52d59395aae0443a0b13a7/README.md#contributing
[dco]: https://github.com/bloomberg/.github/blob/main/DCO.md
[upstream-issue]: https://github.com/bloomberg/pytest-memray/issues/160
[aggregation-pr]: https://github.com/bloomberg/pytest-memray/pull/107
[release]: https://github.com/bloomberg/pytest-memray/releases/tag/1.6.0
[stats]: https://bloomberg.github.io/memray/stats.html
[flamegraph]: https://bloomberg.github.io/memray/flamegraph.html
