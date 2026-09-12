---
project-code: full-captures
project-color: orange
repository: jeremycarroll/pytest-memray
base-branch: main
human-lead: Jeremy Carroll
issue: 100-101
status: proposed
source-revision: 34dd4eacd6cd839d67a0ea133815ee3badff67c1
source-read-date: 2026-09-12
---

# Full-fidelity Memray captures: requirements and design

This is the canonical requirements/design proposal for
[Full-fidelity Memray captures][project], commissioned by [100-101][issue].
Acceptance of this document locks the decisions below for [100-102][plan-ticket].
It specifies the product contract and verification obligations; it does not
create an implementation plan, DAG, implementation tickets, or software changes.

## Goal and user workflow

Let users explicitly request non-aggregated Memray captures for allocation-level
analysis while keeping aggregated captures as the default.
[Upstream issue #160][upstream-issue] describes retaining per-test binaries with
`--memray-bin-path`, including runs with `--native` and
`--trace-python-allocators`, then attempting temporal flame graphs. The issue also
requests access to statistics that require individual allocation records.

The change provides `--memray-full` and the Boolean setting `memray_full`.
When enabled, every capture already produced by pytest-memray uses
`FileFormat.ALL_ALLOCATIONS`. Otherwise it continues to use
`FileFormat.AGGREGATED_ALLOCATIONS`.

Full means Memray's non-aggregated file format within the existing tracking
window and allocator settings. It does not mean every allocation outside that
window is captured or that Python allocator tracing is enabled automatically.
Memray's ordinary flame graph represents a memory snapshot, normally the peak;
its temporal reporter permits selection of a time range. This design does not
promise that a full capture alone makes every function visible in a peak report.
See the [Memray flame graph documentation][flamegraph-docs].

## Scope and boundaries

In scope are configuration registration/resolution, the Tracker format argument,
regression and persisted-capture tests, user documentation, a release-note
fragment, and evidence for a reviewed upstream submission or handoff.

Out of scope:

- Changing the aggregated default, existing tracking activation, tracking window,
  marker semantics, summaries, capture naming, cleanup, or worker coordination.
- New reporters, temporal visualization code, CSV pipelines, or custom binary
  readers and writers.
- Isolating a subregion of a test. Users needing that retain application-level
  `memray.Tracker` control, as discussed in issue #160.
- Environment-variable configuration for the new setting, aliases, additional
  markers, and unrelated configuration repairs or refactoring.
- Performance guarantees or a benchmark project. Documentation must explain the
  potential storage and runtime cost without inventing measurements.
- Deployment, package publication, upstream merge, or closing issue #160 without
  upstream maintainer acceptance.

## Requirements

| ID  | Required behavior                                                                                                                                                     | Acceptance    |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| R1  | Preserve aggregated captures when the new setting is absent or false. Existing users need no migration.                                                               | AC1, AC3, AC6 |
| R2  | Offer one explicit full-capture opt-in through CLI and pytest configuration, with deterministic precedence and clear invalid-input behavior.                          | AC1, AC2      |
| R3  | Change only the format of captures that existing activation rules already produce. Preserve independent native/Python allocator tracing choices and marker overrides. | AC3, AC6      |
| R4  | Retain usable full-format per-test binaries through `--memray-bin-path`, preserving existing path/prefix, overwrite, metadata and cleanup rules.                      | AC4           |
| R5  | Demonstrate an allocation-level downstream workflow on a real plugin-produced full capture and record its exact command and Memray version.                           | AC5           |
| R6  | Document the interface, precedence, persistence, allocator/tracking boundaries, downstream example, and increased file size/potential runtime overhead.               | AC7           |
| R7  | Deliver a reviewed fork change and upstream submission or concrete human handoff referencing Bloomberg issue #160. Record acceptance accurately.                      | AC8           |

## Locked decisions

These are design decisions for review, not claims of existing implementation or
upstream approval. No further product choice is delegated to plan-project.

| ID  | Decision and rationale                                                                                                                                                                                                         | Enforcement owner/artifact                                   |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| D1  | Use `--memray-full` and `memray_full`. A positive Boolean opt-in is concise and follows the repository's hyphenated CLI/underscored ini convention. Do not add `--memray-no-aggregate`, an enum, or an environment interface.  | Plugin configuration, help, configuration tests and docs; R2 |
| D2  | Default to aggregated. The CLI flag sets true; an absent flag falls back to the Boolean ini value, whose default is false. Preserve the disk-space motivation of [PR #107][aggregation-pr].                                    | Configuration resolution and Tracker tests; R1–R3            |
| D3  | The setting changes capture format only. It neither enables tracking nor requires a persistence path. Marked tests use it even when `--memray` is absent; unmarked tests still need existing tracking activation.              | Tracker integration and activation tests; R3                 |
| D4  | Keep one format choice at the existing Tracker construction point. Do not convert files afterward or introduce a second capture pipeline. Preserve asynchronous wrapping, retries and worker behavior.                         | `src/pytest_memray/plugin.py`; R3–R4                         |
| D5  | Keep existing dependency bounds (`pytest>=8.0`, `memray>=1.19.1`) and supported platforms/interpreters. Verify compatibility as execution work; do not preemptively raise a minimum or silently fall back to aggregation.      | Compatibility evidence; E1                                   |
| D6  | Use `memray stats` as the mandatory reporter acceptance workflow; temporal flame graph generation is a useful additional demonstration. One successful stats workflow satisfies the project's at-least-one-reporter criterion. | Persisted-capture integration test/evidence; AC5             |
| D7  | Warn about larger captures and potential runtime overhead in CLI help/user docs. No new per-test runtime warnings, output changes, or numeric performance promises.                                                            | README, configuration docs and release note; AC7             |
| D8  | Task branches and PRs target `main` in `jeremycarroll/pytest-memray`. Upstream submission follows fork validation/review; Jeremy Carroll owns any permission or maintainer handoff.                                            | PR and finalization evidence; AC8                            |

## Configuration contract

Register `--memray-full` in the existing memray option group as a value-free,
`store_true` flag, with destination `memray_full` and an absent-value default of
`None`. Register `memray_full` as a pytest Boolean ini setting defaulting to false.
Support both `pytest.ini` and `[tool.pytest.ini_options]` in `pyproject.toml` via
pytest's own configuration reader. No new configuration parser is needed.

The effective setting follows the existing `value_or_ini` precedence. In the
current code, a CLI default of false would mask a true ini value because the
helper returns any non-`None` CLI value. The new option must use `None` for
absence; changing defaults of unrelated options is outside this project.

There is a second integration constraint: `value_or_ini` catches `ValueError`
from `getini`. Validate the new Boolean ini setting explicitly during plugin
configuration, converting an invalid value into a pytest `UsageError` naming
`memray_full`. Then resolve CLI/ini precedence and retain the selected format.
Do this before constructing the Manager's result directories or starting any
Tracker. Validate the new ini value even when CLI true would take precedence.
Leave the shared helper and unrelated ini semantics unchanged.

| CLI input                                       | Effective ini value                  | Result when tracking is active                          |
| ----------------------------------------------- | ------------------------------------ | ------------------------------------------------------- |
| Absent                                          | Absent/default false                 | `AGGREGATED_ALLOCATIONS`                                |
| Absent                                          | false                                | `AGGREGATED_ALLOCATIONS`                                |
| Absent                                          | true                                 | `ALL_ALLOCATIONS`                                       |
| `--memray-full`                                 | false or true                        | `ALL_ALLOCATIONS`; explicit CLI opt-in wins             |
| Repeated `--memray-full`                        | Valid Boolean                        | `ALL_ALLOCATIONS`; repetition is harmless               |
| Absent, with `-o memray_full=false`             | File contains true                   | `AGGREGATED_ALLOCATIONS`; pytest's ini override applies |
| `--memray-full -o memray_full=false`            | false                                | `ALL_ALLOCATIONS`; CLI opt-in still wins                |
| `--memray-full=false` or another attached value | Any                                  | Pytest usage error: the flag accepts no value           |
| Absent or present                               | Invalid Boolean, such as `sometimes` | Pytest usage error before capture setup                 |

Use pytest's accepted Boolean forms; do not introduce custom coercion. To disable
an ini opt-in for one invocation, omit the positive flag and use
`-o memray_full=false`. There is no separate negative CLI flag. These precedence
rules resolve potentially conflicting inputs without a new conflict policy.

Examples below specify the interface to be implemented; they have not been run
against the unchanged source revision.

```shell
# One invocation, with persistent captures and both tracing options.
python -m pytest --memray --memray-full --native --trace-python-allocators \
  --memray-bin-path .memray tests/
```

```ini
[pytest]
memray_full = true
```

```toml
[tool.pytest.ini_options]
memray_full = true
```

For either file configuration example, invoke
`python -m pytest --memray --memray-bin-path .memray tests/`. The explicit
`--memray` keeps the example independent of unrelated existing ini activation
behavior. The full setting alone is not an activation switch.

## Capture design and compatibility

Resolve the selected `FileFormat` once per pytest configuration. Pass it to the
existing `tracker_kwargs["file_format"]` used by `Manager.pytest_pyfunc_call`.
Both synchronous and asynchronous paths already share this construction. Keep
the existing native and Python allocator arguments and the optional object
lifetime argument unchanged. In particular, `limit_leaks` still forces native
and Python allocator tracing; full mode adds no such override.

The default format is explicitly supplied rather than relying on Memray's own
Tracker default. Existing FileReader-based summaries and marker checks keep
reading the resulting file. A small real-capture test must verify those readers
work in full mode; mocking the argument alone does not prove compatibility.

Continue to use the existing `--memray-bin-path` and `--memray-bin-prefix`
handling, including parametrized tests and filename truncation. Do not infer
file format from file size or extension: both modes produce `.bin` files. With
no persistent path, existing temporary-directory lifetime remains in effect.
The existing internal `MEMRAY_RESULT_PATH` worker mechanism is unaffected and
is not a new public full-mode setting.

Full format does not expand supported operating systems, Python versions or
Memray APIs. The current code includes object lifetime tracking on supported
Python versions; exercise that path in its existing applicable CI environment.
Do not gate full mode behind that feature's Python-version requirement.

## Acceptance criteria and verification

These are requirements for the eventual implementation. Source inspection in
this design ticket is not execution evidence for any future feature test.

| ID  | Required verification                                             | Pass condition                                                                                                                                                                                                                                                                                                                                                                                               |
| --- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AC1 | Configuration/help tests using the existing pytester suite        | Help exposes CLI and Boolean ini names. Absent/false/true values, CLI-over-ini, `-o` overrides and repeated flags match every valid row of the configuration table. Both pytest.ini and pyproject.toml opt-ins produce full mode.                                                                                                                                                                            |
| AC2 | Invalid/conflicting-input tests                                   | Attached flag values and invalid ini Booleans produce pytest usage errors with the new setting identified. Invalid ini also fails with CLI true and without tracking activation. Valid conflicts resolve as specified; no capture is started for invalid input.                                                                                                                                              |
| AC3 | Tracker construction and activation tests                         | With real Tracker wrapping where practical, exercise both formats × native on/off × Python allocator tracing on/off (eight combinations), asserting all three arguments. Full alone leaves an unmarked test untracked; a marker-activated test honors full without `--memray`.                                                                                                                               |
| AC4 | Persisted binary integration tests in fresh temporary directories | Run a passing allocating test and a parametrized case in both modes with `--memray-bin-path`. Binaries survive pytest exit, are nonempty and readable, correspond to the expected test cases, and retain existing prefix/metadata behavior. Retain existing overwrite, long-name and cleanup regression coverage.                                                                                            |
| AC5 | Allocation-level reporter test on a plugin-produced binary        | `python -m memray stats CAPTURE.bin` exits successfully and reports positive allocation data from a known allocating fixture in full mode. Record Python, pytest and Memray versions, exact capture/reporter commands, target SHA and output. On the same supported Memray version, the corresponding aggregated capture is rejected for lack of full data. Do not assert a full version-specific traceback. |
| AC6 | Relevant integration/regression coverage plus configured CI       | Default behavior remains compatible. Full mode works with high-watermark summary/limit_memory, limit_leaks and its tracing override, async execution, and worker configuration propagation. Exercise object lifetime tracking where supported. Existing tests for retries, xdist, marker conflicts, temporary captures and output continue to pass.                                                          |
| AC7 | User-doc review, Markdown formatting and docs CI                  | README and configuration.rst describe both names, defaults, activation, precedence/disable override, persistence and cost. Include a supported reporter example and distinguish whole-test capture from manual Tracker isolation. Add a towncrier feature fragment using the actual future upstream PR number when available.                                                                                |
| AC8 | Fork and upstream handoff evidence                                | Required current-head checks and fresh configured Cadence review pass, mandatory feedback is resolved, and the fork PR is ready. Record the fork PR, upstream submission URL or exact Jeremy-owned submission handoff, plus any maintainer decision. References use Bloomberg issue #160 explicitly and do not claim it closed before acceptance.                                                            |

Prefer focused extensions of `tests/test_pytest_memray.py` and existing fixtures
over a new test framework. For AC3, extend the current native/Python allocator
argument assertions without losing default-mode coverage. For AC4–AC5, use a
subprocess so the reporter reads a closed capture after pytest exits. Identify
the binary by inspecting the fresh output directory, rather than guessing a
generated prefix or using a glob that also selects metadata.

A reporter verification record should include commands equivalent to:

```shell
python -c 'import sys, pytest, memray; print(sys.version); print(pytest.__version__); print(memray.__version__)'
python -m pytest --memray --memray-full --memray-bin-path CAPTURE_DIR TEST_FILE
python -m memray stats CAPTURE.bin
```

`CAPTURE_DIR`, `TEST_FILE`, and `CAPTURE.bin` stand for the actual isolated fixture
directory, test and emitted file; record their resolved values. The
[stats CLI][stats-docs] documents the reporter interface. The implementation
owner must verify it with the installed supported version; no such run is
claimed here. An additional demonstration may run
`python -m memray flamegraph --temporal -o REPORT.html CAPTURE.bin`, recording a
successful command and generated HTML. Browser interaction is not necessary to
prove the chosen stats acceptance criterion.

## Validation and delivery constraints

The selected-base `.symphony.cfg.json` identifies Linear team `100` and omits
`ci.mode`, selecting native validation. There is no ticket-specific Docker
override: use relevant local checks, Docker for environment gaps, then mandatory
published-head CI. Passing local checks permit the explicit record
`Docker: skipped — passed locally`. Do not change repository configuration for
this feature or substitute local results for CI.

The configured required checks at the recorded source revision are:

| Workflow                                     | Required check names                                                                                                                                 | Configured emitting App ID |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `.github/workflows/build_dist.yml` (`Build`) | `Source and wheel distributions`                                                                                                                     | 15368                      |
| `.github/workflows/build.yml` (`Run`)        | `check docs`, `lint`, `test py38`, `test py39`, `test py310`, `test py311`, `test py312`, `test py312-cov`, `test py313`, `test py314`, `test py315` | 15368                      |

These are configured obligations, not observed passing runs. Re-read the selected
base configuration and applicable branch rules when executing; retain run URLs,
attempts, head SHA, App provenance and required child results. Zizmor is not a
required project check. Cadence is separate from product CI; the repository's
configured preference is Codex through the reviewer App `hackcadence`, with
actual provider/run evidence still to be observed.

For this requirements artifact, check Markdown formatting, metadata parsing,
requirement/acceptance references, source completeness and scope. The document
does not add a new runtime path; application behavior and reporter acceptance
are verified by implementation work. The current publication/access status and
actual validation results belong in the [Codex workpad][issue], not in a claim
that this proposed interface already exists.

## Material assumptions and open decisions

Assumptions selected from the project brief and source conventions:

- The desired unit remains one test invocation with pytest-memray's current
  tracking boundaries. Full-mode storage cost is an explicit user tradeoff.
- A Boolean opt-in suffices for this two-format requirement; no future format
  selector or environment interface is commissioned.
- Existing APIs and dependency bounds can support the new format selection.
  Verification is required; an observed incompatibility must be documented and
  addressed without silently changing the default or weakening acceptance.
- A successful stats workflow satisfies the minimum downstream acceptance;
  temporal visualization remains a supported motivating use case, not new UI
  implementation work.

There are no unresolved material product decisions. The choices above are
reviewable decisions of this artifact. A later human revision can supersede them
with its source and rationale recorded. Compatibility findings that require a
new public contract or dependency floor require an explicit design amendment;
ordinary tool discovery does not.

## Execution inputs and owners

These items must be assigned by the eventual plan. They are verification or
access tasks, not unanswered product questions or reasons to block unrelated
work.

| ID  | Input or verification                                                                                                                                                                                                             | Owner                                  | Dependent work only                                                                             |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| E1  | Observe installed Python/pytest/Memray versions; verify AC1–AC6 at the existing Memray minimum on a compatible interpreter and in the repository's normal supported CI environments. Record any dependency-resolution limitation. | Implementation/validation owner        | Compatibility claims and final acceptance                                                       |
| E2  | Resolve real emitted capture paths and run the stats acceptance command; retain command output and any optional temporal HTML artifact.                                                                                           | Implementation/validation owner        | Reporter evidence and verified documentation example                                            |
| E3  | Discover current check/App/run IDs, branch rules and fresh Cadence verdict; check all feedback surfaces.                                                                                                                          | PR owner                               | Ready-for-human-review handoff                                                                  |
| E4  | Obtain actual fork/upstream PR identifiers and choose the release-note filename under existing towncrier conventions.                                                                                                             | PR/finalization owner                  | PR linkage, final news filename and upstream handoff record                                     |
| E5  | Restore runtime author App repository access if unavailable; verify publication and required labels. No alternate credentials are assumed.                                                                                        | Jeremy Carroll, with Symphony readback | Authenticated publication and CI/review evidence; independent design/testing can proceed        |
| E6  | Confirm upstream submission permission and contribution signoff; submit the reviewed change or deliver exact submission instructions to Jeremy.                                                                                   | Finalization owner / Jeremy Carroll    | Upstream submission only; no package release or upstream merge is required for independent work |

## Source inputs

All required product sources were read on 2026-09-12. Repository source reads
refer to `jeremycarroll/pytest-memray@34dd4eacd6cd839d67a0ea133815ee3badff67c1`.
API pagination for the issue comments and PR files/reviews was exhausted.

| ID  | Source and read evidence                                                                                                                                                                                                                   | Design use                                                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| S1  | [Linear project brief][project] and [100-101][issue], full description/content via Linear GraphQL                                                                                                                                          | Goal, exclusions, acceptance, delegated configuration choice and project metadata                                               |
| S2  | [Bloomberg issue #160][upstream-issue], body and all four comments via public GitHub API; latest comment updated 2026-01-13                                                                                                                | Allocation-level use case, explicit opt-in and persistence/tracing combination                                                  |
| S3  | [PR #107][aggregation-pr], body, all three file patches and submitted review; merged 2024-01-31 as `c329fff3e0125c390bcc836613506cf53e040f0a`                                                                                              | Default-format change and its disk-space rationale                                                                              |
| S4  | [Release 1.6.0][release], complete release body; published 2024-04-18                                                                                                                                                                      | Confirms inclusion of the aggregated-capture change; conversational version recollections are not the release boundary evidence |
| S5  | [plugin.py][plugin-source], [utils.py][utils-source]                                                                                                                                                                                       | Activation, Tracker arguments, configuration precedence, persistence, markers and workers                                       |
| S6  | [tests/test_pytest_memray.py][tests-source]                                                                                                                                                                                                | Existing pytester, Tracker wrapping, file, marker, xdist, retry and async regression patterns                                   |
| S7  | [README.md][readme-source] and [docs/configuration.rst][config-source]                                                                                                                                                                     | Public naming, configuration, platform and contribution conventions                                                             |
| S8  | `pyproject.toml`, `tox.ini`, `Makefile`, `docker-compose.yml`, `.symphony.cfg.json`, `.github/workflows/build.yml`, `.github/workflows/build_dist.yml`, `SYMPHONY.md`, PR template and `.github/symphony/REVIEW.md` at the source revision | Dependency floor, docs/news/test setup, CI, branching and review requirements                                                   |
| S9  | Official Memray [stats][stats-docs] and [flame graph][flamegraph-docs] documentation                                                                                                                                                       | Reporter syntax and snapshot/temporal distinction; runtime compatibility remains E1–E2                                          |
| S10 | Supplied hosted runtime instructions and installed shared `docs/engineering/symphony/proof-of-work.md`, `pull-requests.md`, and `docs/engineering/review/cadence-ai-review.md` under `SYMPHONY_TOOLING_ROOT`                               | Current execution, evidence and acceptance contract                                                                             |

The four issue comments read were [3727697217][comment-1],
[3736726434][comment-2], [3737237769][comment-3], and [3742617066][comment-4].
The discussion's sample `metadata.some_stats` is illustrative user code, not a
verified Memray API contract; the acceptance workflow uses the documented stats
reporter instead. The linked third-party file-I/O guide is background to that
workaround, not a required source for this design.

### Source inputs unavailable

No required product input is unavailable. Browser retrieval of PR #107 and the
release initially returned a cache miss; direct public GitHub API reads succeeded.
This was a retrieval-path limitation, not a missing source.

The project brief also lists historical setup provenance at
`/Users/jeremy/hackathon/symphony-example/scripts/symphony/runtime-bundle/workflow/WORKFLOW.md@0d0d496`.
That author-machine path does not exist on this worker. Its historical contents
were not read or inferred. The supplied current runtime contract and shared
installed guidance govern this issue; no product conclusion depends on that
historical snapshot. Reproducing that exact setup would require Jeremy to
provide it and is outside this project's product requirements.

GitHub author App binding failed with HTTP 404 during this turn. Public source
access succeeded. E5 gates publication, CI and review evidence; it does not
change the design or constitute upstream maintainer approval.

## Consumption by plan-project

[100-102][plan-ticket] should use the accepted revision of this file as its
requirements source, preserve R1–R7 and D1–D8, and map every AC1–AC8 and E1–E6 to
an accountable work item or finalization obligation. Scope may be grouped into
a small number of coherent implementation tasks using the shared Symphony
planning tools. This document supplies no topology, ticket payloads or branch
ancestry exceptions. No independent product judgment remains for the planner.

[project]: https://linear.app/1000lines/project/full-fidelity-memray-captures-b6e86c398fab
[issue]: https://linear.app/1000lines/issue/100-101/create-requirements-and-design-doc
[plan-ticket]: https://linear.app/1000lines/issue/100-102
[upstream-issue]: https://github.com/bloomberg/pytest-memray/issues/160
[aggregation-pr]: https://github.com/bloomberg/pytest-memray/pull/107
[release]: https://github.com/bloomberg/pytest-memray/releases/tag/1.6.0
[comment-1]: https://github.com/bloomberg/pytest-memray/issues/160#issuecomment-3727697217
[comment-2]: https://github.com/bloomberg/pytest-memray/issues/160#issuecomment-3736726434
[comment-3]: https://github.com/bloomberg/pytest-memray/issues/160#issuecomment-3737237769
[comment-4]: https://github.com/bloomberg/pytest-memray/issues/160#issuecomment-3742617066
[plugin-source]: https://github.com/jeremycarroll/pytest-memray/blob/34dd4eacd6cd839d67a0ea133815ee3badff67c1/src/pytest_memray/plugin.py
[utils-source]: https://github.com/jeremycarroll/pytest-memray/blob/34dd4eacd6cd839d67a0ea133815ee3badff67c1/src/pytest_memray/utils.py
[tests-source]: https://github.com/jeremycarroll/pytest-memray/blob/34dd4eacd6cd839d67a0ea133815ee3badff67c1/tests/test_pytest_memray.py
[readme-source]: https://github.com/jeremycarroll/pytest-memray/blob/34dd4eacd6cd839d67a0ea133815ee3badff67c1/README.md
[config-source]: https://github.com/jeremycarroll/pytest-memray/blob/34dd4eacd6cd839d67a0ea133815ee3badff67c1/docs/configuration.rst
[stats-docs]: https://bloomberg.github.io/memray/stats.html
[flamegraph-docs]: https://bloomberg.github.io/memray/flamegraph.html
