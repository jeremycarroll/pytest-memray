# Clean full-captures contribution branch

[100-113 / FC-D](https://linear.app/1000lines/issue/100-113) publishes the accepted
full-capture feature as a clean contribution for Bloomberg issue #160.
Jeremy reviews this preparation record on **fork main** and the linked artifact.
The [artifact branch](https://github.com/jeremycarroll/pytest-memray/tree/full-captures-upstream) is published at
**`9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`**, with one new product-only commit on observed upstream main.
It is an **unsigned review artifact**, without a DCO signoff or upstream PR.

## Authority and exact refs

Jeremy accepted [R2 review 5187789026](https://github.com/jeremycarroll/pytest-memray/pull/8#pullrequestreview-5187789026)
at `4ad23afc66c5a82ed959cd939e7b4e06af1f67d6`, merged as
`2acb32b6b1afa4c17770263e103c73dc893f84f9`. That is this task branch's selected
base; its PR targets `main` and adds only this record. The accepted
[execution contract](https://github.com/jeremycarroll/pytest-memray/blob/4ad23afc66c5a82ed959cd939e7b4e06af1f67d6/docs/symphony-plans/full-captures-execution-contract.md)
and [delivery record](https://github.com/jeremycarroll/pytest-memray/blob/4ad23afc66c5a82ed959cd939e7b4e06af1f67d6/docs/symphony-plans/full-captures-delivery.md)
remain unchanged. FC-C/100-106 is Done; Jeremy accepted PR7 head
`9d66e4975ef3406b67db46fba9048e3ded186a62`, merged as the source snapshot below.
[100-108](https://linear.app/1000lines/issue/100-108) created and read back
106→113→114; its unmerged annotation work is absent from this task branch.

| Ref                                        | Observed value                                                                         |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| Refreshed Bloomberg main / artifact parent | `92a9c85ccbeba900fd52d59395aae0443a0b13a7`                                             |
| Accepted fork source snapshot              | `4b47fd033ac826a9bb28ba8c64cd8d9de7bd1029`                                             |
| Published artifact head                    | `9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`                                             |
| Artifact tree                              | `e96ee97305d4c02732e0b2859edc0ce1b99468f3`                                             |
| Exact input patch SHA256                   | `a28d4565a7f83e21b7a2be6fb80fb953020b421fa5d3846a4a85fe7e4e87e0fc`                     |
| FC-A product source                        | `7d6e9d23a0ba9d4dd0149a00318e3e0405ef4df9`                                             |
| FC-B product sources                       | `2dd12fb97f93f5ee56a35d3489e4092b88eba669`, `952484cd111c9ec1d992b27998c842c139e8853c` |

Immutable review links: [new commit](https://github.com/jeremycarroll/pytest-memray/commit/9cb7f4814daf9a50dec0101b2fc592c7ea2a0346),
[complete product diff and included history](https://github.com/jeremycarroll/pytest-memray/compare/92a9c85ccbeba900fd52d59395aae0443a0b13a7...9cb7f4814daf9a50dec0101b2fc592c7ea2a0346),
[excluded fork divergence and history](https://github.com/jeremycarroll/pytest-memray/compare/92a9c85ccbeba900fd52d59395aae0443a0b13a7...4b47fd033ac826a9bb28ba8c64cd8d9de7bd1029),
and [source tree](https://github.com/jeremycarroll/pytest-memray/tree/4b47fd033ac826a9bb28ba8c64cd8d9de7bd1029). Upstream remained at the recorded base
when refreshed for construction. Check it again before final handoff; advancement
requires an explicit new base/tree/diff and scoped validation, with any
behavior-changing conflict resolution paused.

## Removal by exclusion

The regenerated `git diff --name-status` between the recorded upstream and fork
source has **48 rows: six included and 42 excluded**. No fork history or working
file was deleted. Construction starts at upstream and applies only the accepted
product patch. Every other path remains byte-identical to upstream, including its
own license, workflows and the upstream version of `.github/workflows/zizmor.yml`.

| Source status | Exact path at the source snapshot                                                         | Artifact decision                                |
| ------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------ |
| A             | `.agents/skills/cadence-onboarding/SKILL.md`                                              | Exclude fork-added path                          |
| A             | `.agents/skills/cadence-onboarding/scripts/check-credentials.mjs`                         | Exclude fork-added path                          |
| A             | `.agents/skills/linear-graphql/SKILL.md`                                                  | Exclude fork-added path                          |
| A             | `.agents/skills/linear-graphql/agents/openai.yaml`                                        | Exclude fork-added path                          |
| A             | `.agents/skills/linear-graphql/scripts/linear-graphql.mjs`                                | Exclude fork-added path                          |
| A             | `.agents/skills/symphony-project-factory/SKILL.md`                                        | Exclude fork-added path                          |
| A             | `.agents/skills/symphony-project-factory/templates/project-description.md`                | Exclude fork-added path                          |
| A             | `.agents/skills/symphony-project-factory/templates/tickets/broaden-fanout-integration.md` | Exclude fork-added path                          |
| A             | `.agents/skills/symphony-project-factory/templates/tickets/plan-project.md`               | Exclude fork-added path                          |
| A             | `.agents/skills/symphony-project-factory/templates/tickets/requirements-and-design.md`    | Exclude fork-added path                          |
| A             | `.agents/skills/symphony-project-factory/templates/tickets/standup.md`                    | Exclude fork-added path                          |
| A             | `.agents/skills/symphony-project-factory/templates/tickets/trigger-fan-out.md`            | Exclude fork-added path                          |
| A             | `.copier-answers.yml`                                                                     | Exclude fork-added path                          |
| A             | `.gitattributes`                                                                          | Exclude fork-added path                          |
| A             | `.github/pull_request_template.md`                                                        | Exclude fork-added path                          |
| A             | `.github/symphony/APP-SETUP.md`                                                           | Exclude fork-added path                          |
| A             | `.github/symphony/REVIEW.md`                                                              | Exclude fork-added path                          |
| A             | `.github/symphony/cadence-app-manifest.json`                                              | Exclude fork-added path                          |
| A             | `.github/symphony/setup-app.mjs`                                                          | Exclude fork-added path                          |
| A             | `.github/symphony/symphony-app-manifest.json`                                             | Exclude fork-added path                          |
| A             | `.github/workflows/cadence-ai-review-events.yml`                                          | Exclude fork-added path                          |
| A             | `.github/workflows/cadence-ai-review-trigger.yml`                                         | Exclude fork-added path                          |
| A             | `.github/workflows/cadence-ai-review.yml`                                                 | Exclude fork-added path                          |
| A             | `.github/workflows/cadence-linear-rework.yml`                                             | Exclude fork-added path                          |
| A             | `.github/workflows/cadence-review-check-cleanup.yml`                                      | Exclude fork-added path                          |
| A             | `.github/workflows/cadence-review-ingress.yml`                                            | Exclude fork-added path                          |
| A             | `.github/workflows/symphony-client-setup.yml`                                             | Exclude fork-added path                          |
| A             | `.github/workflows/symphony-client-wakeups.yml`                                           | Exclude fork-added path                          |
| M             | `.github/workflows/zizmor.yml`                                                            | Exclude fork modification; retain upstream bytes |
| A             | `.symphony.cfg.json`                                                                      | Exclude fork-added path                          |
| M             | `README.md`                                                                               | Include accepted product diff                    |
| A             | `SYMPHONY.md`                                                                             | Exclude fork-added path                          |
| M             | `docs/configuration.rst`                                                                  | Include accepted product diff                    |
| A             | `docs/engineering/symphony/pull-requests.md`                                              | Exclude fork-added path                          |
| A             | `docs/engineering/symphony/replanning.md`                                                 | Exclude fork-added path                          |
| A             | `docs/news/160.feature.rst`                                                               | Include accepted product diff                    |
| A             | `docs/symphony-plans/fan-out-100-103-mapping.md`                                          | Exclude fork-added path                          |
| A             | `docs/symphony-plans/fan-out-plan-100-102-full-captures.md`                               | Exclude fork-added path                          |
| A             | `docs/symphony-plans/fan-out-plan-100-102-full-captures.mmd`                              | Exclude fork-added path                          |
| A             | `docs/symphony-plans/full-captures-delivery.md`                                           | Exclude fork-added path                          |
| A             | `docs/symphony-plans/full-captures-execution-contract.md`                                 | Exclude fork-added path                          |
| A             | `docs/symphony-plans/full-captures-requirements-design.md`                                | Exclude fork-added path                          |
| A             | `scripts/symphony/fetch-pr-progress.mjs`                                                  | Exclude fork-added path                          |
| A             | `scripts/symphony/render-pr-progress.mjs`                                                 | Exclude fork-added path                          |
| A             | `scripts/symphony/runtime-bundle/skills/symphony-replan/SKILL.md`                         | Exclude fork-added path                          |
| M             | `src/pytest_memray/plugin.py`                                                             | Include accepted product diff                    |
| M             | `tests/test_object_tracking.py`                                                           | Include accepted product diff                    |
| M             | `tests/test_pytest_memray.py`                                                             | Include accepted product diff                    |

The later R2 planning commits and this FC-D record are also excluded by the
allowlist. No Symphony configuration, local environment, capture, validation log,
build output or worktree metadata is in the artifact's tracked contribution.
All six product files match both accepted fork source and FC-C's actually tested
`0b2d99061f49ad125e84577780b01a3a4edcf3e3` byte for byte.

## Complete excluded and included commit history

All **22 commits** in the baseline fork divergence below are absent from artifact
ancestry. This includes the three product source commits: their exact changes
were reapplied, rather than their commits copied. Later fork-only commits are
excluded for the same reason. The task branch preserves this history on main.

Executed `git log --format='%H %s' 92a9c85ccbeba900fd52d59395aae0443a0b13a7..4b47fd033ac826a9bb28ba8c64cd8d9de7bd1029`:

```text
4b47fd033ac826a9bb28ba8c64cd8d9de7bd1029 Merge pull request #7 from jeremycarroll/symphony/full-captures/100-106/finalize-full-captures
9d66e4975ef3406b67db46fba9048e3ded186a62 [100-106] Track clean delivery and upstream submission follow-up
274743e6ccb3d5435367b90570cd8830dc312fa7 [100-106] Record combined validation and upstream submission handoff
0b2d99061f49ad125e84577780b01a3a4edcf3e3 Merge remote-tracking branch 'origin/main' into symphony/full-captures/100-106/finalize-full-captures
4b142113925fb9fd21cc5012e395fa2eebaef28f Merge pull request #5 from jeremycarroll/symphony/full-captures/100-105/full-capture-docs
fbc946f7effcdb5cd32339303c40129f9bef07d0 [100-106] Prepare delivery evidence and upstream handoff requirements
bacc18945d555b1d8c40e08d5632330888eb364e Merge remote-tracking branch 'origin/main' into symphony/full-captures/100-105/full-capture-docs
c09c1c2e56e48cecb5cec0f191c36c02f5f87341 Merge pull request #6 from jeremycarroll/symphony/full-captures/100-104/full-capture-selection
952484cd111c9ec1d992b27998c842c139e8853c [100-105] Record verified Memray stats versions
7d6e9d23a0ba9d4dd0149a00318e3e0405ef4df9 Add opt-in full allocation captures and regression coverage
cd3080e3fcbb00c9325c341b71e219c8bf480615 Merge pull request #4 from jeremycarroll/symphony/full-captures/100-103/annotate-fan-out
2dd12fb97f93f5ee56a35d3489e4092b88eba669 docs: explain full captures and downstream reporting
6e83a698123768f918ccfd6f9e012b7f86957c8d [100-103] Record full-captures ticket fan-out
874241401eb4016be2d1179785b58f17d997c829 Merge pull request #3 from jeremycarroll/symphony/full-captures/100-102/fan-out-plan
d403161792521f57d9a633c09b99c9d07fd5c1a2 [100-102]: plan full capture implementation and upstream handoff
09d23352e875d3981117a80ba25632d377187c2c Merge pull request #2 from jeremycarroll/symphony/full-captures/100-101/requirements-design
33eaf3f7706ee22618c35ddbe65b6b9773ed7d1f [100-101]: remove resolved publication blocker from design
d14e3c1a8db647500d3006daf6afe70d40956d10 [100-101]: document full-capture requirements and design
34dd4eacd6cd839d67a0ea133815ee3badff67c1 Merge pull request #1 from jeremycarroll/chore/add-symphony-client
2fb5c3b3d96a0f7efbd61475ca5e5e9a0720b470 Disable automatic zizmor checks
d708407340ff24a5c08b0f59365f0e4bcb6811e5 Use existing CI for Symphony checks
7f83eaa648e8d9b81f04f6d80b68ba8f00afa89e Add Symphony client configuration
```

The complete `git log --format='%H %s' 92a9c85ccbeba900fd52d59395aae0443a0b13a7..9cb7f4814daf9a50dec0101b2fc592c7ea2a0346` is:

```text
9cb7f4814daf9a50dec0101b2fc592c7ea2a0346 Add opt-in full allocation captures
```

The parent is exactly upstream main; `git rev-list --count` returns **1**.
An ancestry-set comparison confirmed no baseline fork-only commit is included.
GitHub's commit API independently read back the parent, tree and all six files.

## Construction and publication evidence

Executed in issue workspace
`/var/lib/symphony/code/1000lines-symphony-workspaces/100-113`, with task checkout
`repo/`, artifact worktree `clean-artifact/`, patch `full-captures.patch`,
environment `.venv/` and logs `evidence/`. From `repo/`:

```shell
git fetch https://github.com/bloomberg/pytest-memray.git main:refs/remotes/upstream/main
git diff --binary 7d6e9d23^ 7d6e9d23 -- \
  src/pytest_memray/plugin.py tests/test_pytest_memray.py tests/test_object_tracking.py \
  > ../full-captures.patch
git diff --binary c09c1c2 4b14211 -- \
  README.md docs/configuration.rst docs/news/160.feature.rst >> ../full-captures.patch
sha256sum ../full-captures.patch
git worktree add -b full-captures-upstream ../clean-artifact 92a9c85ccbeba900fd52d59395aae0443a0b13a7
cd ../clean-artifact
git apply --check ../full-captures.patch
git apply --index ../full-captures.patch
git diff --cached --check
git diff --cached --name-status
git diff --cached --stat
git write-tree
git commit -m "Add opt-in full allocation captures"
git diff --check 92a9c85ccbeba900fd52d59395aae0443a0b13a7 HEAD
git push origin HEAD:refs/heads/full-captures-upstream
git ls-remote origin refs/heads/full-captures-upstream
```

All application/whitespace checks passed. The unchanged-base checksum, tree and
counts match the accepted baseline exactly; no conflict or product edit occurred.
The artifact branch and associated upstream PR were absent before construction;
a second remote-absence check immediately preceded the push. Readback returned:

```text
9cb7f4814daf9a50dec0101b2fc592c7ea2a0346 refs/heads/full-captures-upstream
```

GitHub confirms author and committer
`1000lines-symphony[bot] <326272204+1000lines-symphony[bot]@users.noreply.github.com>`.
The commit has **no Signed-off-by trailer**; local signature status is `N` and
GitHub verification is `verified: false, reason: unsigned`. Jeremy's fork
acceptance is not DCO certification. No global identity was changed.

```text
 README.md                     |  64 +++++++
 docs/configuration.rst        |  95 +++++++++++
 docs/news/160.feature.rst     |   4 +
 src/pytest_memray/plugin.py   |  30 +++-
 tests/test_object_tracking.py |  25 +--
 tests/test_pytest_memray.py   | 381 +++++++++++++++++++++++++++++++++++++++---
 6 files changed, 560 insertions(+), 39 deletions(-)
```

## Local validation and installed provenance

Configured/effective mode **native/native**, no ticket Docker override.
**Docker: skipped — passed locally.** Dependency groups came from the artifact's
unchanged `pyproject.toml`. A noneditable install of artifact `9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`
produced pytest-memray **1.10.1.dev3+g9cb7f4814** in workspace `.venv` site-packages.
Python **3.9.25**, pytest **8.4.2**, Memray **1.20.0**. This installed ref is
separate from historical FC-C installed/tested `0b2d99061f49ad125e84577780b01a3a4edcf3e3`
and any later task documentation SHA.

| Command / target                                                                          | Result and evidence                                                                |
| ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Artifact `make check PYTEST_ARGS='-p root_isolation --basetemp=.cache/fc-d/pytest-check'` | 198 passed, 12 interpreter skips; `evidence/artifact-check.log`                    |
| Artifact `make lint`                                                                      | Ruff, Black and mypy pass; `evidence/artifact-lint.log`                            |
| Artifact `make docs`                                                                      | Sphinx/linkcheck pass; `evidence/artifact-docs.log`                                |
| Artifact `pipx run build[virtualenv] --sdist --wheel`                                     | Both distributions built at version above; `evidence/artifact-build.log`           |
| Artifact `python -m towncrier build --draft --version 0.0.0`                              | Feature160 rendered; no tracked news generation; `evidence/artifact-towncrier.log` |
| Environment `python -m pip check`                                                         | No broken requirements                                                             |
| Artifact `git diff --check` against recorded upstream                                     | Pass; no other tracked changes                                                     |

The disposable root-isolation hook follows FC-C's accepted environment recipe:
after pytester initializes, set nested `PYTEST_ADDOPTS=--rootdir=.`. It keeps
nested tests workspace-local without changing tracked tests/configuration.
`TMPDIR` is workspace `.venv/tmp`. Pipx's default man directory was unwritable;
workspace-local `PIPX_HOME`, `PIPX_BIN_DIR`, `PIPX_MAN_DIR` and `XDG_CACHE_HOME`
resolved that environment setup failure before the successful build.

The unchanged three plugin/test files retain [FC-A minimum/object proof](https://linear.app/1000lines/issue/100-104#comment-3851c547-6549-421e-bb66-61c74214d36b):
Memray1.19.1/Python3.9.25, 162 targeted passes and 12 skips; all12 object cases
passed separately on Python3.13.15/pytest9.1.1/Memray1.19.1 in the recorded
container digest. That historical evidence covers unchanged behavior; it is not
relabeled as execution of this new artifact SHA. Current-head CI covers the
supported interpreter matrix. Temporal HTML was optional and not generated.

## Fresh full and aggregated reporter execution

From `clean-artifact/`, the fresh fixture
`.cache/fc-d/reporter/test_allocations.py` has an adjacent empty `[pytest]` config:

```python
def test_allocations():
    buffers = [bytearray(4096) for _ in range(20)]
    assert sum(map(len, buffers)) == 81920
```

Executed with `.venv/bin` first on PATH; emitted paths were discovered from the
sole `.bin` in each fresh directory, excluding metadata:

```shell
python -m pytest --memray --memray-full --native --trace-python-allocators --memray-bin-path .cache/fc-d/reporter/full .cache/fc-d/reporter/test_allocations.py
python -m memray stats .cache/fc-d/reporter/full/ecb7cab7a87a43f18e18a0ff6aaed454-test_allocations.py-test_allocations.bin
python -m pytest --memray --native --trace-python-allocators --memray-bin-path .cache/fc-d/reporter/aggregated .cache/fc-d/reporter/test_allocations.py
python -m memray stats .cache/fc-d/reporter/aggregated/bbf62b24a41649ebbadd2faf1747f42a-test_allocations.py-test_allocations.bin
```

Both capture tests passed. FileReader confirmed `ALL_ALLOCATIONS` versus
`AGGREGATED_ALLOCATIONS`, with native and Python-allocator tracing enabled in both.
Full stats exited **0**: **75 allocations, 85.896kB total, 84.388kB peak**.
Aggregated stats exited **1**, as expected:
`NotImplementedError: Can't compute statistics using a pre-aggregated capture file.`
Complete commands, stdout and metadata remain in `evidence/reporter.json`;
these values are fixture observations, not performance guarantees.

## Published checks and review gate

Artifact checks target `9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`, event **push**, ref
`full-captures-upstream`, GitHub Actions **App15368**, attempt **1**:
[Run34716011559](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559)
(`.github/workflows/build.yml`) and
[Build34716011472](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011472)
(`.github/workflows/build_dist.yml`). **All12 required children passed** on this artifact head.

| Required child                 | Result  | Job evidence                                                                                             |
| ------------------------------ | ------- | -------------------------------------------------------------------------------------------------------- |
| Source and wheel distributions | success | [103613262060](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011472/job/103613262060) |
| lint                           | success | [103613262466](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262466) |
| test py312-cov                 | success | [103613262559](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262559) |
| check docs                     | success | [103613262590](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262590) |
| test py314                     | success | [103613262689](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262689) |
| test py38                      | success | [103613262694](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262694) |
| test py310                     | success | [103613262700](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262700) |
| test py39                      | success | [103613262703](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262703) |
| test py312                     | success | [103613262719](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262719) |
| test py311                     | success | [103613262733](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262733) |
| test py315                     | success | [103613262775](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262775) |
| test py313                     | success | [103613262777](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559/job/103613262777) |

The main-based task PR separately requires Prettier on this file, `make docs`,
whitespace validation and all12 current-head Run/Build checks. The
[pinned workpad](https://linear.app/1000lines/issue/100-113#comment-e45900d2-b863-4991-86f3-828aed516ce1)
and task PR record exact task SHAs, each required child/job, run attempts,
feedback closure and current-head Cadence evidence. No task check substitutes
for artifact CI. Fork main is unprotected with no additional branch rules at
readback. Manual zizmor and release-only upload_pypi are excluded; neither was
triggered. Artifact workflows are upstream's own; no Symphony workflows were copied.

Cadence preference is Codex, reviewer App hackcadence. Its fresh task-head review
must explicitly cover artifact `9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`, this inventory and
its linked diff/history/evidence. Human handoff additionally requires closed
mandatory feedback, a clean task branch, ready PR, orange/symphony labels and
jeremycarroll assignment. These gates remain pending until verified in the workpad.

## Acceptance freeze and next owner

The published artifact SHA above is the candidate to freeze; **Jeremy's acceptance
of that exact artifact and this record is pending**. FC-D remains its sole writer.
Record Jeremy's actual review URL, accepted SHA, Done state and task-main merge
in the pinned workpad before transferring ownership to
[FC-E / 100-114](https://linear.app/1000lines/issue/100-114).

FC-E must read back the accepted remote SHA before mutation. Jeremy supplies real
DCO certification and authorized submission access there. Any certification
replacement must preserve this parent/tree, use the exact observed-old-SHA lease,
and receive fresh artifact checks and review. Only an actual upstream PR number
can authorize the later fragment rename. No upstream PR, signoff, merge/closure,
release/tag/PyPI, hosted deploy or completed project is claimed by this record.
