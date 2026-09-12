# Full-captures execution and evidence contract

Part of the [100-102 fan-out plan](./fan-out-plan-100-102-full-captures.md).
The plan defines topology, ownership and task content; this document defines
the common instructions, validation and source provenance to carry into each
generated ticket. Both documents require the same human plan review.

## Shared ticket execution contract

100-108 must copy this section, the validation environment below, and the exact
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
  renderer for the accepted five-node implementation plan, with verified links, observed issue
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
  independent preparation by FC-D/FC-E. Missing real DCO and submission
  authority gate only FC-E's dependent writes; a prepared package is not submission.

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

100-108 pins the human-accepted R2 plan commit, rereads sources and seed state, and
uses the shared `tools/symphony-dag` modules for graph validation and payload
rendering. Verify team/project/assignee, main ref, Backlog/Active/Inactive/Unhappy
states, orange/mature/wake labels, and GitHub orange/symphony definitions before
issue or relation writes. Required labels may be created with existing authority
and read back; missing access, mapping, refs or direction fails closed.

Reuse FC-A/100-104, FC-B/100-105 and FC-C/100-106 exactly as Done history;
create only FC-D and FC-E. The manifest's `existing_issue` and `issue_id` prevent
core payload generation for retained nodes. Inspect existing project issues
before writing; if a retry has already created D/E, reuse those IDs. Override
Active to Backlog for staging, persist each returned UUID/identifier/URL, copy
complete node content and shared sections, then verify labels, Jeremy assignment,
source links and bodies. Read back existing A/B→C relations; create only C→D and
D→E, bind observed UUIDs and read both directions before activation. No mutation
of completed seeds or new design seed. On partial failure repair the confirmed
stage rather than duplicate issues. 100-107 does no fan-out writes.

After accepted R2 is merged and 100-107 Done, 100-108 annotates both graph copies
with actual D/E identifiers and extends the existing mapping record with a
clearly dated R2 section; retain original acceptance/creation evidence. If those
annotations need a PR, it is `symphony/full-captures/100-108/apply-delivery-replan`
from/to main, draft, orange/symphony and Jeremy assigned, with docs/graph/payload
checks, all12 CI and fresh Cadence. Annotations do not change the accepted R2 topology or branch bases;
workers resolve their actual IDs from verified fan-out readbacks and never
commit unmerged annotation work into delivery task branches.
Seed hard relations 106→107→108 already exist separately; no extra seed or
redundant implementation relations are created.

Completion gates: FC-A retains AC1–AC6/E1–E2; FC-B retains AC7 and provisional E4;
FC-C retains accepted combined validation and patch evidence. Each current PR
owner covers E3/E5. FC-D owns accepted clean-branch publication/review; FC-E owns
actual upstream PR, final E4/E6, observed-number rename and submission checks.
The old patch package alone does not satisfy amended AC8. No missing input can
be converted into a success claim; only a human scope amendment changes this
endpoint. Maintainer acceptance/merge is outside scope and not claimed.

## R2 ownership and branch lifecycle

| Resource or file                                                      | FC-D preparation                       | Transfer event                             | FC-E submission                                                                                          |
| --------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `docs/symphony-plans/full-captures-delivery.md`                       | Read accepted FC-C record              | None; historical evidence retained         | Read only                                                                                                |
| `docs/symphony-plans/full-captures-clean-branch.md`                   | Create and review on main task PR      | D accepted, Done and record merged         | Read exact accepted ref                                                                                  |
| Fork `refs/heads/full-captures-upstream`                              | Create/publish one product-only commit | D accepted frozen SHA and record on main   | Sole coordinated writer; certification and exact rename                                                  |
| Six product files on artifact                                         | Apply exact patch; no feature changes  | Accepted parent/tree/head/checks           | Preserve tree except observed-number fragment rename; changed upstream base requires revalidation/review |
| `docs/symphony-plans/full-captures-upstream-submission.md`            | No write                               | D→E                                        | Create evidence/prepared body on main-based task PR                                                      |
| `docs/news/160.feature.rst` and one resolved destination on fork main | No write                               | Actual upstream PR number observed by E    | Rename only, matching artifact                                                                           |
| One upstream PR to `bloomberg/pytest-memray:main`                     | No write                               | Real certification and verified permission | Create/read back, final checks and scoped feedback                                                       |

Jeremy owns the repository/branch resource and human acceptance. The assigned
Symphony worker owns each task's preparation, checks and evidence. Submission or
certification operations that require Jeremy are executed by his authorized
account; his exact result is read back by FC-E. No second approval of the overall
delivery direction is required.

The branch name is **full-captures-upstream** in **jeremycarroll/pytest-memray**.
At execution, inspect whether it or an associated upstream PR exists. If absent,
FC-D may create it from the observed upstream SHA. If present, reuse only when
its ownership/base/head and workpad match this contribution; unexpected state
pauses its dependent write for Jeremy rather than overwriting another branch.
Record remote before/after refs. It contains upstream history plus one new
product-only commit, never fork task/merge commits. FC-D may publish under the
actual App author identity without claiming human DCO. If unsigned, it is a
review artifact only until Jeremy certifies it in FC-E.

Per Jeremy's [PR #10 review](https://github.com/jeremycarroll/pytest-memray/pull/10#pullrequestreview-5187981207),
FC-D's **main-based task PR** prepares a concise upstream PR body, matching the
granularity of merged upstream contributions, with one link back to the fork PR.
The artifact contains only the accepted product change; no Symphony client
template, working files, planning or handoff records accompany it. Keep the
exclusion inventory, exact refs/checksum and individual CI jobs in the fork
PR/workpad and immutable history. The short preparation document retains the
artifact commit/compare links and actual unsigned status outside the proposed body.
Record Jeremy's review of that exact artifact SHA. Cadence must inspect it and
the linked evidence. All task PR bases stay main; no PR targets the artifact.

After D acceptance/Done/main merge, FC-E compares the remote to the accepted SHA
before mutation. A genuine certification replacement changes the SHA even with
identical tree; record both, compare parent/tree, rerun all12 artifact checks,
and obtain fresh review covering the new SHA in the main-based E PR/workpad.
Only the sole known unsigned preparation commit may be replaced, by Jeremy,
with explicit `--force-with-lease=refs/heads/full-captures-upstream:<observed-old-sha>`.
Never rewrite unrelated/upstream commits. Once submitted, add the signed-off
fragment rename as a normal descendant commit. Preserve the branch while the
upstream PR uses it; no automatic deletion, reset, upstream merge or release.
Jeremy owns later retention and maintainer-response work after project handoff.

## Product allowlist and exact exclusions

Upstream base refreshed by 100-107 on 2026-09-12:
`92a9c85ccbeba900fd52d59395aae0443a0b13a7`. Accepted fork source main:
`4b47fd033ac826a9bb28ba8c64cd8d9de7bd1029`. Source FC-A commit:
`7d6e9d23a0ba9d4dd0149a00318e3e0405ef4df9`; FC-B product commits:
`2dd12fb97f93f5ee56a35d3489e4092b88eba669` and
`952484cd111c9ec1d992b27998c842c139e8853c`. The exact patch is reproducible from
these accepted changes using the merged delivery record's commands. SHA256:
`a28d4565a7f83e21b7a2be6fb80fb953020b421fa5d3846a4a85fe7e4e87e0fc`.
Six files, **560 additions/39 deletions**, resulting tree:
`e96ee97305d4c02732e0b2859edc0ce1b99468f3`.
100-107 reproduced that checksum and cached application/tree on refreshed
upstream main; no delivery branch or submission was created by that validation.

The complete allowed product diff is:

```text
src/pytest_memray/plugin.py
tests/test_pytest_memray.py
tests/test_object_tracking.py
README.md
docs/configuration.rst
docs/news/160.feature.rst
```

All other paths remain byte-identical to the observed upstream base. This means
preserving upstream's own workflows/license/product files, not deleting them.
The following inventory is the complete 48-row fork delta at
`92a9c85..4b47fd0`: include the six allowlisted product rows and omit the other
42 working paths from the contribution diff. For the modified zizmor path,
retain the upstream version. Every later planning/record file, including the new FC-D/FC-E
records, is also excluded by the allowlist.

```text
A	.agents/skills/cadence-onboarding/SKILL.md
A	.agents/skills/cadence-onboarding/scripts/check-credentials.mjs
A	.agents/skills/linear-graphql/SKILL.md
A	.agents/skills/linear-graphql/agents/openai.yaml
A	.agents/skills/linear-graphql/scripts/linear-graphql.mjs
A	.agents/skills/symphony-project-factory/SKILL.md
A	.agents/skills/symphony-project-factory/templates/project-description.md
A	.agents/skills/symphony-project-factory/templates/tickets/broaden-fanout-integration.md
A	.agents/skills/symphony-project-factory/templates/tickets/plan-project.md
A	.agents/skills/symphony-project-factory/templates/tickets/requirements-and-design.md
A	.agents/skills/symphony-project-factory/templates/tickets/standup.md
A	.agents/skills/symphony-project-factory/templates/tickets/trigger-fan-out.md
A	.copier-answers.yml
A	.gitattributes
A	.github/pull_request_template.md
A	.github/symphony/APP-SETUP.md
A	.github/symphony/REVIEW.md
A	.github/symphony/cadence-app-manifest.json
A	.github/symphony/setup-app.mjs
A	.github/symphony/symphony-app-manifest.json
A	.github/workflows/cadence-ai-review-events.yml
A	.github/workflows/cadence-ai-review-trigger.yml
A	.github/workflows/cadence-ai-review.yml
A	.github/workflows/cadence-linear-rework.yml
A	.github/workflows/cadence-review-check-cleanup.yml
A	.github/workflows/cadence-review-ingress.yml
A	.github/workflows/symphony-client-setup.yml
A	.github/workflows/symphony-client-wakeups.yml
M	.github/workflows/zizmor.yml
A	.symphony.cfg.json
M	README.md
A	SYMPHONY.md
M	docs/configuration.rst
A	docs/engineering/symphony/pull-requests.md
A	docs/engineering/symphony/replanning.md
A	docs/news/160.feature.rst
A	docs/symphony-plans/fan-out-100-103-mapping.md
A	docs/symphony-plans/fan-out-plan-100-102-full-captures.md
A	docs/symphony-plans/fan-out-plan-100-102-full-captures.mmd
A	docs/symphony-plans/full-captures-delivery.md
A	docs/symphony-plans/full-captures-execution-contract.md
A	docs/symphony-plans/full-captures-requirements-design.md
A	scripts/symphony/fetch-pr-progress.mjs
A	scripts/symphony/render-pr-progress.mjs
A	scripts/symphony/runtime-bundle/skills/symphony-replan/SKILL.md
M	src/pytest_memray/plugin.py
M	tests/test_object_tracking.py
M	tests/test_pytest_memray.py
```

The inventory above is the complete observed fork delta, with its six product
rows included to make the exclusion decision reviewable: **include only the six
allowlisted rows; exclude the other 42**. Regenerate `git diff --name-status
<observed-upstream> <accepted-fork-main>` in D and mark every row include/exclude.
Commit exclusion is exact: all **22 commits in
`92a9c85ccbeba900fd52d59395aae0443a0b13a7..4b47fd033ac826a9bb28ba8c64cd8d9de7bd1029`**
are excluded as ancestry, including the three product source commits (their diff
is reapplied) and all merges, onboarding, plan, mapping and delivery commits.
Record `git log --format='%H %s' <base>..<head>` for both fork divergence and
artifact; the latter must contain only the new product commit before submission.
Deleting working files from a fork-main copy would not meet this history test.

## Clean branch recipe — FC-D only

These are planned commands, not claimed execution. Use full observed SHAs in the
record; regenerate the source patch first with the exact two `git diff --binary`
commands in the merged delivery record. Run in the issue workspace and put the
artifact worktree, environment and outputs beneath it. No global Git identity
change. The task branch remains on main; the artifact gets a separate worktree.

```shell
git fetch https://github.com/bloomberg/pytest-memray.git main:refs/remotes/upstream/main
git rev-parse refs/remotes/upstream/main
sha256sum ../full-captures.patch
git worktree add -b full-captures-upstream ../clean-artifact OBSERVED_UPSTREAM_SHA
cd ../clean-artifact
git apply --check ../full-captures.patch
git apply --index ../full-captures.patch
git diff --cached --check
git diff --cached --name-status
git diff --cached --stat
git write-tree
git commit -m "Add opt-in full allocation captures"
git log --format=fuller OBSERVED_UPSTREAM_SHA..HEAD
git diff --check OBSERVED_UPSTREAM_SHA HEAD
git push origin HEAD:refs/heads/full-captures-upstream
git ls-remote origin refs/heads/full-captures-upstream
```

Resolve the local patch location to the actual workspace path before running.
Commit with the actual worker identity; no `--signoff` or Jeremy authorship is
implied here. Check branch absence/ownership before `worktree add` or push.
If upstream advances, the old checksum still verifies the input patch but the
result tree must be observed anew. Record conflicts and pause any resolution
that would change accepted product behavior; ordinary application/testing is
execution input. Recheck current upstream before handoff/submission.

For each relevant check use the repository commands as executable/argument
arrays, cwd the artifact or task as specified by its node:

```json
[
  ["make", "check"],
  ["make", "lint"],
  ["make", "docs"],
  ["pipx", "run", "build[virtualenv]", "--sdist", "--wheel"],
  ["python", "-m", "towncrier", "build", "--draft", "--version", "0.0.0"],
  ["git", "diff", "--check"]
]
```

Use the delivery record's allocating fixture and actual full/aggregated stats
workflow. The accepted installed/tested source **0b2d99061f49ad125e84577780b01a3a4edcf3e3**
(Python3.9.25, pytest8.4.2, Memray1.20.0) and FC-A minimum/object proof remain
separate from every new package install, task document SHA and artifact SHA.
Run relevant checks locally, Docker only for environment gaps using the existing
Validation environment recipe, then all12 App15368 Run/Build jobs on **both**
published task and artifact heads. Artifact push workflows come from upstream;
do not copy Symphony config/review workflows into the clean branch. Its CI must
be linked into the main-based task review, not substituted by task-head CI.

## Submission and certification recipe — FC-E only

Observed upstream main is protected; the branch response exposes empty required
status contexts/checks and `/rules/branches/main` returns `[]`. This does not
prove absence of all upstream PR gates. Current Run/Build source and emitted
checks match the 12-job baseline (App15368). Refresh workflow sources, branch
metadata/rules, commit checks/statuses and actual PR rollup at execution. Include
additional emitted/required checks such as DCO; observe App/check names instead
of inventing them. Missing permission to read a required rule gates the affected
submission/handoff and needs Jeremy's exact rule readback. Do not trigger release
or zizmor just to obtain an unrelated success signal.

No repository PR/contribution template exists at upstream `92a9c85`, but
**bloomberg/.github@6e6478c5f719f8ac2251558635f700dd5c0f128e** supplies the
[actual organization PR template](https://github.com/bloomberg/.github/blob/6e6478c5f719f8ac2251558635f700dd5c0f128e/PULL_REQUEST_TEMPLATE.md),
[contribution instructions](https://github.com/bloomberg/.github/blob/6e6478c5f719f8ac2251558635f700dd5c0f128e/CONTRIBUTING.md)
and [DCO](https://github.com/bloomberg/.github/blob/6e6478c5f719f8ac2251558635f700dd5c0f128e/DCO.md).
Read the current versions and actual submission form again in E. The existing
README requires real-name signoff on every commit, and links an issue reference
in the PR summary. Existing issue160 satisfies the feature-request source;
create no duplicate upstream issue. Template sections are issue number,
**Describe your changes**, **Testing performed**, **Additional context**.
FC-E prepares `upstream-pr.md` outside the artifact's tracked tree with those
sections, issue `#160`, unchanged public contract, exact tested/version evidence,
limitations and check links. Use FC-D's concise proposed body and refresh its
testing evidence for the final submitted head. Its single fork PR link retains
development history; internal inventories and handoff notes stay in the fork.
Title: **Add opt-in full allocation captures**. No automatic closing keyword.

Before upstream create, Jeremy reads the actual contribution and DCO, confirms
his right to submit, and supplies his real author identity/certification. If the
D artifact is unsigned, Jeremy uses his own authenticated checkout to replace
that sole commit with the same parent/tree and a genuine signoff. The prepared
operation is `git commit --amend --signoff --reset-author --no-edit` under his
verified Git identity, followed by inspection of every commit in base..head.
He publishes with the explicit observed-old-SHA lease described above. FC-E
records parent/tree equality, old/new SHA, authors and actual Signed-off-by
trailers, reruns all12 checks and records fresh review of the new exact artifact.
Adding a signed acknowledgement after an unsigned commit is insufficient.

Separately verify submission permission using the authorized identity: for
Jeremy's account, `gh api user` must identify him, fork push access must work,
and cross-fork PR creation must be permitted. Upstream collaborator write access
is not inherently needed to submit a cross-fork PR, but the runtime's fork App
grant does not prove it can perform that operation. Prior FC-C author-App bind
to upstream returned HTTP404; it is historical denied access, not current proof.
Do not mint another token to expand installation grants or borrow Jeremy's PAT.
If the runtime lacks authorized submission access, Jeremy performs the exact
prepared command below using his own account, then provides the URL for API
readback. This is the specific missing-input handoff, not a second approval of
the already accepted direction.

```shell
gh pr create --repo bloomberg/pytest-memray --base main   --head jeremycarroll:full-captures-upstream   --title "Add opt-in full allocation captures" --body-file upstream-pr.md
```

Before retrying, search existing PRs for that head. Read back actual URL/number,
base, head repository/ref/SHA, files and every commit/signoff. Name that observed
number N in the workpad before performing `git mv docs/news/160.feature.rst
docs/news/N.feature.rst` on both artifact and E's main-based task branch. N is
substituted from the response, never guessed. If N=160, retain the file and
record why no rename is needed; if destination exists unexpectedly, stop that
write and resolve the collision. Jeremy signs off the artifact rename commit;
the Symphony task commit uses its actual identity. Text is unchanged and all
other fragments are excluded. No generated `docs/news.rst` or release action.

Rerun towncrier/docs/whitespace locally, Docker for gaps only, then all12 fork
artifact/task checks and upstream's observed required checks on the final PR
head. Read submitted reviews, inline threads, conversation and fresh Linear
feedback. A certification rewrite or rename cannot reuse prior-SHA review/CI as
current evidence. The main E PR/workpad links final artifact and upstream heads
for fresh Codex/hackcadence review. Missing access/certification/checks leaves
actual submission or acceptance pending with exact Jeremy action and readback;
never label a prepared package as submitted. Jeremy owns final acceptance/Done,
and upstream maintainers own any later merge or issue closure.

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
Prettier. Record actual commands/results in 100-107's workpad and PR, followed
by all configured current-head CI. This document makes no future feature-test
success claim.

The installed shared renderer emits core metadata and source links but omits
inline node scope, file lists, acceptance and commands. Its JSON preview is
therefore **inspection-only, not a complete live ticket body**. 100-108 must
copy the exact reviewed new-node fields and shared execution/validation sections
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

## R2 source and feedback ledger — 2026-09-12

- Full current project brief and 100-107/108 scope, 104/105/106 Codex/Cadence
  workpads, PR5/6/7 bodies, submitted reviews, conversations, inline comments
  and resolved/outdated threads read. Inline threads are empty; no fresh human
  Linear instruction. Jeremy review5187653118 is the authorized amendment;
  current admin permission was reverified. PR7 reply5648021675 already records
  the larger-replan choice, followed by accepted/Done106 and merge4b47fd0.
- Accepted plan/design/execution contract at d403161, current main4b47fd0,
  accepted delivery record at that merge, original fan-out mapping, existing
  replanning guide/template, README/SYMPHONY/config/review guidance, actual fork
  template, toolchain/Make/tox/Compose and all relevant workflows read.
- FC-A7d6e9d2 and FC-B bacc189 human/Cadence acceptance remain retained; FC-B
  evidence F1 is closed. PR7's product-evidence F1 was closed at274743e; that
  approval predates the delivery amendment. Human approval5187678521 and merge
  accept9d66e49; do not relabel older Cadence evidence as its current-head review.
  AR-100-106-handoff-F1 and the human amendment are implemented in R2's D/E
  ownership and direct dependencies; future execution remains owned by D/E.
- Upstream issue160/all4 comments through3742617066, PR107/body/three patches,
  release1.6.0, current upstream README and official stats/flamegraph docs read.
  Upstream main92a9c85 and org6e6478c5 trees are complete (not truncated).
  Organization template/contribution/DCO files were found and read; no invented
  repository template. Current upstream Run/Build jobs/App15368 and branch/rules
  observations are recorded above; FC-E refreshes actual PR requirements.
- No required source is unavailable. Initial GraphQL request-shape error and
  config-helper/display invocation errors were corrected. Historical author
  machine WORKFLOW provenance remains optional as the accepted design states.
  DCO/submission permission is an execution gate for E, not missing plan source.
- Unchanged shared tooling c5c36da145f169dc4d1f223a470727784f140ff6 was cloned and
  built inside the 100-107 workspace because installed tooling lacked dist and
  dependencies. No project-local planner or shared process edits were made.
