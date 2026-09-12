# Full-capture delivery record

Combined implementation and documentation validation for [100-106][finalizer],
under the accepted [plan][plan] and [design][design]. The product-only upstream
package is prepared below; Jeremy owns its signoff and submission. The final
fork review is [PR #7][pr-c], targeting **main**. No deployment or package release
is required.

## Accepted refs and provenance

Both predecessor issues are Done and both PRs were approved and merged by Jeremy.
Their 12 required checks pass on their respective accepted heads; the matching
Cadence workpads close all mandatory predecessor findings.

| Input                | Accepted head                              | Merge into main                                                     | Review evidence                                                              |
| -------------------- | ------------------------------------------ | ------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [FC-A / PR #6][pr-a] | `7d6e9d23a0ba9d4dd0149a00318e3e0405ef4df9` | `c09c1c2e56e48cecb5cec0f191c36c02f5f87341`, 2026-09-12 18:06:03 UTC | [Cadence approval][review-a], [Jeremy approval][human-a], [workpad][proof-a] |
| [FC-B / PR #5][pr-b] | `bacc18945d555b1d8c40e08d5632330888eb364e` | `4b142113925fb9fd21cc5012e395fa2eebaef28f`, 2026-09-12 18:42:00 UTC | [Cadence approval][review-b], [Jeremy approval][human-b], [workpad][proof-b] |

FC-C originally branched from main `c09c1c2`; this combined audit starts from
fetched main **`4b142113925fb9fd21cc5012e395fa2eebaef28f`**. Both accepted heads
are verified ancestors. Merging main into the existing task branch produced
**`0b2d99061f49ad125e84577780b01a3a4edcf3e3`**, without conflicts. All six product
files match combined main byte for byte. FC-C changes only this delivery record;
product correction and cleanup commits: **none**.

The actual installed/tested revision is `0b2d99061f49ad125e84577780b01a3a4edcf3e3`:
editable pytest-memray `0.1.dev158+g0b2d99061`, resolving to this workspace's
`src/pytest_memray`. Python **3.9.25**, pytest **8.4.2**, Memray **1.20.0**.
Later delivery-record commits have separate published-head CI/review provenance
in [PR #7][pr-c] and the pinned [FC-C workpad][proof-c]; they do not change the
executed product source or retroactively change the installed version.

## Acceptance and execution ledger

Configured/effective mode: **native/native**, no ticket Docker override.
Local logs and exact commands are retained under `.cache/fc-c/final/` and their
reviewer-relevant output is copied to the pinned workpad.

| Obligation | Evidence and result                                                                                                                                                                                                                                      |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC1        | Combined configuration tests pass: CLI/INI/TOML, Boolean forms, overrides, repetition and explicit aggregated default.                                                                                                                                   |
| AC2        | Invalid ini fails before Manager/Tracker setup even with CLI true or tracking inactive; attached CLI values are rejected. Combined tests pass.                                                                                                           |
| AC3        | Activation remains independent; tests cover both formats and all native/Python-allocator combinations, including marker overrides.                                                                                                                       |
| AC4        | Real subprocess tests verify persisted binaries, metadata, names/prefixes, overwrite and temporary cleanup; combined tests pass.                                                                                                                         |
| AC5 / E2   | Full capture with both tracing flags produces stats; identical fixture/version without full mode produces the expected aggregated rejection. Exact commands and output below.                                                                            |
| AC6 / E1   | `make check PYTEST_ARGS='-p root_isolation --basetemp=.cache/fc-c/final/pytest-check'`: **198 passed, 12 skipped**. Minimum-version and supported object coverage retained below.                                                                        |
| AC7        | Both guides match the implemented contract; `make docs`, Markdown check and towncrier draft pass. Provisional news identifier has the exact Jeremy-owned rename below.                                                                                   |
| AC8 / E3   | [PR #7][pr-c] and [workpad][proof-c] hold the final published SHA, all 12 required Run/Build results, fresh Codex/hackcadence verdict, feedback closure and ready transition. These remain publication gates; preparation-head approval is insufficient. |
| E4         | Fork PRs #6, #5 and #7 are observed. No upstream PR number exists for this contribution; use the handoff below.                                                                                                                                          |
| E5         | Fork author App access verified; PR #7 has orange/symphony labels and jeremycarroll assignee, with helper/API readback recorded in the workpad.                                                                                                          |
| E6         | Exact product-only source, base, patch verification, proposed title/body, permission and real-signoff actions are provided below. Actual submission is Jeremy-owned.                                                                                     |

`make lint` passed Ruff, Black and mypy (five source files). `make docs` passed
Sphinx/linkcheck. `pipx run build[virtualenv] --sdist --wheel` built
`pytest_memray-0.1.dev158+g0b2d99061.tar.gz` and the matching `py3-none-any.whl`.
`python -m towncrier build --draft --version 0.0.0` rendered the full-capture
feature under issue 160; the existing issue-136 fix is unrelated and unchanged.
`prettier --no-editorconfig --check docs/symphony-plans/full-captures-delivery.md README.md`,
`python -m pip check` and `git diff --check` pass.

The disposable `root_isolation` fixture sets `PYTEST_ADDOPTS=--rootdir=.` only
after each pytester fixture initializes, so nested tests inside the workspace
retain their intended roots. Repository tests/configuration are unchanged.
Lint initially hit `OSError: AF_UNIX path too long`; shortening workspace TMPDIR
to `.venv/tmp` resolved it, and the complete lint target passed.
**Docker: skipped — passed locally** for product validation.

The unchanged plugin/tests retain [FC-A minimum evidence][proof-a]: Python
3.9.25 / pytest 8.4.2 / Memray **1.19.1**, 162 targeted passes and 12 interpreter
skips; both full stats (21 allocations, 82.460 kB total/peak) and aggregated
rejection verified. FC-A also ran all **12 object-tracking cases successfully**
on Python **3.13.15**, pytest **9.1.1**, Memray **1.19.1**, using its recorded
`registry.gitlab.com/python-devs/ci-images@sha256:0c4c476e470fc3b53547e579ac75d90c911b7218a720a88d1fc7d035b5b42fb8`.
FC-C verified those three source/test files are unchanged and inspected accepted
CI, including py313/py314/py315. There is no changed behavior requiring duplicate
minimum/object runs. Final PR CI still covers the full supported matrix.

## Combined reporter evidence

Working directory: `/var/lib/symphony/code/1000lines-symphony-workspaces/100-106`.
`python` resolves to `.venv/bin/python`. Fixture
`.cache/fc-c/final/reporter/test_allocations.py` contains:

```python
def test_allocations():
    buffers = [bytearray(4096) for _ in range(20)]
    assert sum(map(len, buffers)) == 81920
```

An adjacent empty `[pytest]` configuration bounds the fixture's root. Both
output directories were fresh. Each invocation passed its one test, exit 0:

```shell
python -m pytest --memray --memray-full --native --trace-python-allocators \
  --memray-bin-path .cache/fc-c/final/reporter/full \
  .cache/fc-c/final/reporter/test_allocations.py
python -m memray stats .cache/fc-c/final/reporter/full/872690d168c34855ac3443f139a822c8-test_allocations.py-test_allocations.bin
python -m pytest --memray --native --trace-python-allocators \
  --memray-bin-path .cache/fc-c/final/reporter/aggregated \
  .cache/fc-c/final/reporter/test_allocations.py
python -m memray stats .cache/fc-c/final/reporter/aggregated/195d3f159ecf48c688d7bdb5881d2b9b-test_allocations.py-test_allocations.bin
```

Paths were discovered from each directory's sole `.bin`, excluding metadata.
FileReader confirmed `ALL_ALLOCATIONS` versus `AGGREGATED_ALLOCATIONS`; both
captures report native and Python-allocator tracing enabled. Full stats exited 0:

```text
📏 Total allocations:
    75
📦 Total memory allocated:
    85.896kB
📈 Peak memory usage:
    84.388kB
```

Aggregated stats exited 1:

```text
NotImplementedError: Can't compute statistics using a pre-aggregated capture file.
```

These are fixture observations, not performance guarantees. Exact absolute argv,
full stdout/stderr and exit codes are in `reporter/results.json` and the workpad.
Temporal HTML is optional and was not generated; stats satisfies AC5.

## Scoped cleanup

Audited all six merged product paths, this record and the accepted fan-out plan.
The required `rg -n 'TODO|FIXME|stub|adapter|disabled|compat'` search returned no
hits in the six product files. Additional HACK/TEMP/XXX, shim, legacy, rollout,
feature-flag and project-code searches found no temporary integration seam.

The temporary-directory references in plugin help, docs and cleanup tests describe
durable capture lifetime; object-test temporary objects are deliberate fixtures.
The new `memray_full` switch is durable user configuration. Plan/ledger mentions
of compatibility and cleanup are historical requirements/evidence. All are
retained. No unrelated pre-existing code, fragments or planning history changed.
Ignored captures, logs, environment and detached patch-verification worktree are
retained as FC-C evidence. No FC-C task container persists; other workers'
resources were left untouched. No source/host deployment or release is claimed.

## Jeremy-owned upstream package

Target: `bloomberg/pytest-memray`, **main** at observed/refreshed
**`92a9c85ccbeba900fd52d59395aae0443a0b13a7`** on 2026-09-12.
Contribution source is FC-A `7d6e9d23a0ba9d4dd0149a00318e3e0405ef4df9` plus
FC-B `2dd12fb97f93f5ee56a35d3489e4092b88eba669` and
`952484cd111c9ec1d992b27998c842c139e8853c`; merge commits only establish acceptance.
No FC-C product correction is needed.

From a clone containing the accepted fork history, reproduce the exact patch:

```shell
git diff --binary 7d6e9d23^ 7d6e9d23 -- \
  src/pytest_memray/plugin.py tests/test_pytest_memray.py tests/test_object_tracking.py \
  > ../full-captures.patch
git diff --binary c09c1c2 4b14211 -- \
  README.md docs/configuration.rst docs/news/160.feature.rst \
  >> ../full-captures.patch
sha256sum ../full-captures.patch
```

SHA-256: `a28d4565a7f83e21b7a2be6fb80fb953020b421fa5d3846a4a85fe7e4e87e0fc`.
The retained `.cache/fc-c/final/product.patch` has exactly **six files,
560 additions, 39 deletions**. `git apply --check`, `git apply --index` and
`git diff --cached --check` passed in a detached upstream-base worktree.
All six resulting files are byte-identical to accepted combined main; the
resulting upstream tree is `e96ee97305d4c02732e0b2859edc0ce1b99468f3`.
This excludes Symphony onboarding/planning files and all unrelated fork changes.
Do not push fork main as the upstream contribution branch.

The existing author App's upstream binding returned **HTTP 404**; its fork grant
does not authorize upstream submission. No upstream token, PR or write was
obtained. [Upstream contribution instructions][contributing] require real-name
signoff on every commit under the [DCO][dco]. Source commits are App-authored,
without Jeremy's certification. This blocks only actual submission.

After fork PR #7 reaches its CI/Cadence/ready gate, Jeremy must review the patch,
confirm his right to contribute under the DCO, and use his authorized account:

1. Fetch upstream main and verify its SHA. If it has advanced, record the new
   base, reapply the six-file patch and rerun affected checks. Do not silently
   include fork divergence.
2. Create `full-captures-upstream` from the verified upstream base, apply
   `../full-captures.patch` with `git apply --index`, and verify the six-file diff.
3. Verify Git author name/email are his real contribution identity. Only Jeremy
   can certify it with `git commit --signoff -m "Add opt-in full allocation captures"`.
   Inspect every contributed commit's author and signoff; fork approval is not DCO.
4. Verify `gh api user` identifies his authorized account and that he can push
   the clean branch to `jeremycarroll/pytest-memray` and open a cross-fork PR.
   Push that branch, then submit to upstream main with the exact title/body below.
5. Read back PR URL/number, upstream base/head, exact six-file diff and commit
   signoffs. Observe and pass upstream's actual required checks, including DCO
   if required. Fork CI does not substitute for upstream-head CI.
6. Once the upstream PR number is observed, record source
   `docs/news/160.feature.rst` and destination
   `docs/news/<observed-upstream-PR-number>.feature.rst`. Jeremy owns that exact
   `git mv`, preserving feature text and every other fragment. Sign off the
   rename commit, rerun towncrier/docs and current-head required checks, and
   record URL/SHA/check readback in the workpad. No identifier is invented.

Proposed title: **Add opt-in full allocation captures**.
Proposed body (save as `upstream-pr.md`):

```markdown
## Summary

Add --memray-full and Boolean memray_full configuration for allocation-level
reporters. Aggregated captures remain the default; activation and allocator
tracing stay independent. Invalid configuration fails before capture setup.

Tests cover configuration, retained captures, stats, markers, workers, retries,
async execution and supported object tracking. Guides explain precedence,
persistence, tracing boundaries and storage/runtime costs.

References #160.

## Validation

Combined source: jeremycarroll/pytest-memray@4b142113925fb9fd21cc5012e395fa2eebaef28f.
Python 3.9.25 / pytest 8.4.2 / Memray 1.20.0: 198 tests passed, 12 object tests
skipped on this interpreter. Minimum Memray 1.19.1 passed 162 targeted tests;
all 12 object tests passed separately on Python 3.13.15 / Memray 1.19.1.
Lint, Sphinx/linkcheck, sdist/wheel build and towncrier draft passed.
Full captures with both tracing flags produced stats; aggregated captures were
rejected as expected. Fork evidence and final head checks:
https://github.com/jeremycarroll/pytest-memray/pull/7
```

Jeremy's submission command after the gates above:

```shell
gh pr create --repo bloomberg/pytest-memray --base main \
  --head jeremycarroll:full-captures-upstream \
  --title "Add opt-in full allocation captures" --body-file upstream-pr.md
```

[Issue #160][upstream-issue] remains open; all four comments were reread.
[PR #107][aggregation-pr], [release 1.6.0][release], current contribution/DCO
instructions and official [stats][stats]/[flame graph][flamegraph] docs were read.
No maintainer decision on this contribution has been observed. Upstream merge,
issue closure, tagging, PyPI publication and hosted deployment are excluded.
Jeremy owns final project acceptance and any later upstream follow-up.

[finalizer]: https://linear.app/1000lines/issue/100-106
[plan]: https://github.com/jeremycarroll/pytest-memray/blob/d403161792521f57d9a633c09b99c9d07fd5c1a2/docs/symphony-plans/fan-out-plan-100-102-full-captures.md
[design]: https://github.com/jeremycarroll/pytest-memray/blob/d403161792521f57d9a633c09b99c9d07fd5c1a2/docs/symphony-plans/full-captures-requirements-design.md
[pr-a]: https://github.com/jeremycarroll/pytest-memray/pull/6
[pr-b]: https://github.com/jeremycarroll/pytest-memray/pull/5
[pr-c]: https://github.com/jeremycarroll/pytest-memray/pull/7
[proof-a]: https://linear.app/1000lines/issue/100-104#comment-3851c547-6549-421e-bb66-61c74214d36b
[proof-b]: https://linear.app/1000lines/issue/100-105#comment-e09a7ba3-b103-4049-bca8-8e619958ba3c
[proof-c]: https://linear.app/1000lines/issue/100-106#comment-cbac84b4-303c-4e39-a9e3-369eeaaebe39
[review-a]: https://github.com/jeremycarroll/pytest-memray/pull/6#pullrequestreview-5187399243
[human-a]: https://github.com/jeremycarroll/pytest-memray/pull/6#pullrequestreview-5187448227
[review-b]: https://github.com/jeremycarroll/pytest-memray/pull/5#pullrequestreview-5187466169
[human-b]: https://github.com/jeremycarroll/pytest-memray/pull/5#pullrequestreview-5187567161
[contributing]: https://github.com/bloomberg/pytest-memray/blob/92a9c85ccbeba900fd52d59395aae0443a0b13a7/README.md#contributing
[dco]: https://github.com/bloomberg/.github/blob/main/DCO.md
[upstream-issue]: https://github.com/bloomberg/pytest-memray/issues/160
[aggregation-pr]: https://github.com/bloomberg/pytest-memray/pull/107
[release]: https://github.com/bloomberg/pytest-memray/releases/tag/1.6.0
[stats]: https://bloomberg.github.io/memray/stats.html
[flamegraph]: https://bloomberg.github.io/memray/flamegraph.html
