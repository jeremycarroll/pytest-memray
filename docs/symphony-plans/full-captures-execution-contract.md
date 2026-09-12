# Full-captures execution and evidence contract

Part of the [100-102 fan-out plan](./fan-out-plan-100-102-full-captures.md).
The plan defines topology, ownership and task content; this document defines
the common instructions, validation and source provenance to carry into each
generated ticket. Both documents require the same human plan review.

## Shared ticket execution contract

100-103 must copy this section, the validation environment below, and the exact
corresponding plan manifest node content into each generated ticket. Put the node's
summary, creates, edits, exclusions, acceptance checks and validation commands
first. Preserve empty lists as `none`. Include pinned links to this plan and
the design using the accepted plan commit, the node ID, direct blocker and
blocked issue links from the verified mapping, source reads, ownership,
dependencies, delivery notes and the following obligations. Regeneration replaces
the generated content in place; it never appends a second copy.

- Work only in the assigned workspace. Inspect selected-base configuration and
  instructions, the accepted design, all listed sources and fresh human feedback.
  Do not change unrelated configuration, markers, summaries or workflow tooling.
- Branch from main at dispatch and open a draft PR against main when independent
  work is publishable. Never commit predecessor changes absent from main. If an
  upstream result is missing, publish only independent work/dependency notes and
  wait for the named result; do not change the PR base.
- Keep one pinned `## Codex Workpad`, recording base/head SHAs, source reads,
  assumptions, command outcomes, Docker digest/skip, CI/review links, feedback
  ledger, PR labels and next handoff. Required unreadable sources fail closed.
- Every fork PR uses `[<issue>]: <title>`, labels orange and symphony, and assignee
  jeremycarroll. Verify definitions and application with the shared
  `ensure-pr-labels.mjs` helper and API readback. Preserve other labels.
  Required missing labels that current permissions allow are routine setup;
  resolve them before dependent writes. Do not change grants or borrow identity.
- PR bodies explain the user outcome, linked project goal, TL;DR, selected main
  base, accepted plan and concise Tested evidence. Use the shared progress
  renderer for the accepted three-node plan, with verified links, observed issue
  states and a separate current-node highlight. Keep detailed run logs in Linear.
- Validate **local → Docker for environment gaps → mandatory current-head CI**.
  Passing relevant local checks means `Docker: skipped — passed locally`.
  An unrun, skipped, canceled, stale or pending check is never passing evidence.
  Fix known failing assertions before publishing. Record configured/effective
  mode and any explicit ticket override without changing repository defaults.
- Required CI pending/missing: Unhappy with wake:15m. Failure or conflict: Active.
  Passing required CI: Inactive while the configured Cadence review runs.
  Missing access/input: Inactive for only the dependent action, naming the exact
  operation, failure, required permission, Jeremy-owned action and readback.
  The server owns CI waiting; human acceptance owns Done.
- Cadence preference is Codex, reviewer App hackcadence. Normal human handoff
  requires approval of the current PR SHA, matching Cadence workpad/verdict,
  all required checks passing, all mandatory feedback closed, a clean task branch
  and ready-from-draft PR. Inspect submitted reviews, inline comments/threads,
  top-level comments and fresh Linear comments; later review-relevant activity
  needs a fresh review. Request human review only after this closure, or the
  documented three-pass cap with the unresolved question explicitly handed off.
- Apply `mature` to a blocker only at that readiness point. Remove it for
  request-changes, rejected/stale acceptance evidence or a similarly severe
  downstream-invalidating regression; ordinary edits alone do not revoke it.
  Failure to apply/remove a required label is a named API blocker. Maturity does
  not place unmerged code on main or satisfy FC-C's accepted-result requirement.
- Record source refs, installed package refs and actual command execution
  separately. No deployment, release, upstream merge or upstream issue closure
  is authorized by this plan. Missing upstream submission access does not block
  FC-A/FC-B or preparation of FC-C's complete human submission package.

## Validation environment

The baseline `.symphony.cfg.json` has no `ci.mode`, so configured/effective mode
is **native**, with no ticket Docker override. Its build array is
`["bash", "-lc", "pipx run build[virtualenv] --sdist --wheel"]`; its test array
is `["bash", "-lc", "docker compose run --rm test tox"]`. The latter is the
repository container fallback, not an instruction to repeat passing native
checks. Use existing Make/tox targets and a workspace-local Python environment.
Install required dependency groups there using the repository's pyproject.toml;
do not install the whole interpreter matrix on the host.

For a local environment gap, use the documented Compose image
`registry.gitlab.com/python-devs/ci-images:active`. The tag is not immutable:
pull once, record its actual RepoDigest, and use that digest for task runs.
The equivalent isolated invocation is below; `CHECK` is the applicable node's
exact local command, run with `bash -lc`, after environment setup in `/w`.
For tox use the installed matching interpreter environment (for example
`tox -e py312`, `tox -e docs` or `tox -e lint`); record unavailable interpreters.

```shell
docker pull registry.gitlab.com/python-devs/ci-images:active
docker image inspect registry.gitlab.com/python-devs/ci-images:active --format '{{json .RepoDigests}}'
docker run --rm --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$PWD,dst=/w" --workdir /w \
  --env PIP_CACHE_DIR=/w/.cache/pip --env XDG_CACHE_HOME=/w/.cache \
  IMAGE_AT_RECORDED_DIGEST bash -lc CHECK
```

Replace the digest and command arguments with observed values, not literal
placeholders. Mount only the issue checkout, publish no ports, and leave no task
container. Do not prune shared images or other workers' resources. If Docker is
also unavailable, record the exact environment limitation and proceed to the
mandatory CI stage; a failed assertion is not an environment limitation.

Every node, including documentation and final delivery-document changes, must
pass these baseline checks on its published head, plus any applicable branch
rules discovered at execution. Record workflow/event/ref, SHA, run URL/attempt,
emitting App and each required child job. Baseline App is GitHub Actions 15368;
main was unprotected with no extra rule checks at planning time.

| Workflow                                   | Required checks                                                                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `.github/workflows/build.yml` (Run)        | check docs; lint; test py38; test py39; test py310; test py311; test py312; test py312-cov; test py313; test py314; test py315 |
| `.github/workflows/build_dist.yml` (Build) | Source and wheel distributions                                                                                                 |

Zizmor is manual and is not required. Release-only upload_pypi is not required
and must not be triggered. Cadence and routing jobs are separate from product CI.
FC-A/FC-C record Python, pytest and Memray versions for minimum-version and
normal-environment evidence. Use Memray 1.19.1 on a compatible interpreter for
the minimum check; preserve current dependency bounds. Any actual incompatibility
that changes the public contract or dependency floor needs a design amendment.

## Fan-out preflight and completion gates

100-103 pins the human-accepted plan commit, rereads sources and seed state, and
uses the shared `tools/symphony-dag` modules for graph validation and payload
rendering. Verify team/project/assignee, main ref, Backlog/Active/Inactive/Unhappy
states, orange/mature/wake labels, and GitHub orange/symphony definitions before
issue or relation writes. Required labels may be created with existing authority
and read back; missing access, mapping, refs or direction fails closed.

Create exactly FC-A/FC-B/FC-C, temporarily overriding the generated Active state
with verified Backlog for issue creation. Persist each returned UUID, identifier
and URL immediately. Verify the complete set, bind symbolic relation endpoints,
write exactly the two payloads above and read both blocker directions back, then
activate all three unless fresh human input requests a hold. On partial failure,
reuse confirmed IDs and repair the incomplete stage; never infer rollback or
create duplicates. Branch names use the actual identifiers. Annotate only graph
labels with resulting IDs in both graph copies; preserve node IDs, payload keys,
branch templates and edges. The installed parser does not accept click directives,
so retain clickable Linear links in the payload mapping/branch record instead.

Completion gates: FC-A covers AC1–AC6/E1–E2; FC-B covers AC7 and provisional E4;
every PR owner covers E3/E5; FC-C closes AC1–AC8 and E1–E6 with accepted combined
refs, cleanup and actual upstream submission or a complete Jeremy handoff.
An unmet required gate prevents completion or requires explicit human descoping.
No source availability claim substitutes for test execution or upstream acceptance.

## Sources read and unavailable

Read 2026-09-12 unless stated otherwise. Repository reads use baseline
`09d23352e875d3981117a80ba25632d377187c2c`; shared tooling reads use
`c5c36da145f169dc4d1f223a470727784f140ff6` under `SYMPHONY_TOOLING_ROOT`.

| Source                                                                                                            | Evidence and planning use                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Project brief][project], [100-102][planning-ticket], [100-101][design-ticket] and [100-103][fanout-ticket]       | Full Linear descriptions/content, comments, issue states and seed relations; scope, metadata, existing seeds and generation contract                   |
| [Accepted design][design] and [merged PR #2][design-pr]                                                           | R1–R7, D1–D8, AC1–AC8 and E1–E6; merged SHA and Done confirmed, all obligations assigned above                                                         |
| [Bloomberg issue #160][upstream-issue]                                                                            | Body and all four API comments, ending at 3742617066; pagination exhausted; opt-in workflow and native/Python tracing combination                      |
| [PR #107][aggregation-pr]                                                                                         | Body, all three file patches, approval and empty conversation; merged c329fff3e0125c390bcc836613506cf53e040f0a; preserve default/disk-space motivation |
| [Release 1.6.0][release]                                                                                          | Full release body confirms aggregated-capture change; no reliance on conversational version recollection                                               |
| Current plugin.py, utils.py, tests/test_pytest_memray.py, tests/test_object_tracking.py, tests/conftest.py        | Tracker/configuration/activation/persistence/worker behavior and existing test patterns; bound file ownership                                          |
| README.md, configuration.rst, pyproject.toml, tox.ini, Makefile, docker-compose.yml, news template                | Documentation, DCO, dependencies, validation commands and feature-fragment conventions                                                                 |
| SYMPHONY.md, .symphony.cfg.json, Run/Build/Cadence workflows, PR template and .github/symphony/REVIEW.md          | Base, required checks, native mode, review provenance and human handoff; no target AGENTS.md/CLAUDE.md found                                           |
| Shared docs/symphony-plans/{README,fan-out-plan-schema,fan-out-criteria}.md and tools/symphony-dag source/fixture | Existing plan fields, split tradeoffs, parser and rendering behavior                                                                                   |
| Shared proof-of-work.md, pull-requests.md and cadence-ai-review.md                                                | Validation order, current-head evidence and maturity/readiness contract                                                                                |
| Official [stats][stats-docs] and [flame graph][flamegraph-docs] docs                                              | Reporter syntax and whole-test/temporal scope; execution evidence remains FC-A/FC-C work                                                               |

No required product source is unavailable. Browser cache misses for PR #107 and
release 1.6.0 were recovered through the public GitHub API. The accepted design
classifies the brief's author-machine `WORKFLOW.md@0d0d496` path as unavailable
historical setup provenance, not a required product source. Its contents are not
inferred; current supplied runtime and installed shared guidance govern.

## Plan validation and rendering limitation

Use unchanged shared exports `parseProjectPlan`, `parseProjectGraph`,
`parseRelationPayloadTable` and `buildDagLinearPayloadFromMarkdown`. Compare the
standalone graph with the embedded graph, and parsed relation rows with the
manifest-derived payloads. The core plan parser derives relations from edges;
it does not itself validate the prose relation table. A one-off comparison of
those shared parsed outputs supplies that check without adding a new validator.
Review topology/ownership and all AC/E mappings, and format this Markdown with
Prettier. Record actual commands/results in 100-102's workpad and PR, followed
by all configured current-head CI. This document makes no future feature-test
success claim.

The installed shared renderer emits core metadata and source links but omits
inline node scope, file lists, acceptance and commands. Its JSON preview is
therefore **inspection-only, not a complete live ticket body**. 100-103 must
copy the exact reviewed node fields and shared execution/validation sections
into its structured issue inputs, in the stable order specified above, then
inspect/read back the complete descriptions before activation. Pinned links
confirm the source but do not replace inline content. Do not invent missing
requirements or write a project-local renderer/schema. The planning PR proposes
a shared renderer enhancement; that advisory proposal does not gate this plan.

[project]: https://linear.app/1000lines/project/full-fidelity-memray-captures-b6e86c398fab
[planning-ticket]: https://linear.app/1000lines/issue/100-102
[design-ticket]: https://linear.app/1000lines/issue/100-101
[fanout-ticket]: https://linear.app/1000lines/issue/100-103
[design]: ./full-captures-requirements-design.md
[design-pr]: https://github.com/jeremycarroll/pytest-memray/pull/2
[upstream-issue]: https://github.com/bloomberg/pytest-memray/issues/160
[aggregation-pr]: https://github.com/bloomberg/pytest-memray/pull/107
[release]: https://github.com/bloomberg/pytest-memray/releases/tag/1.6.0
[stats-docs]: https://bloomberg.github.io/memray/stats.html
[flamegraph-docs]: https://bloomberg.github.io/memray/flamegraph.html
