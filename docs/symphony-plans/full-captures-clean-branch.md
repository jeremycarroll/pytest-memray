# Add opt-in full allocation captures

Proposed upstream PR body, prepared on fork `main` for Jeremy's review.
The contribution is [commit `9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`](https://github.com/jeremycarroll/pytest-memray/commit/9cb7f4814daf9a50dec0101b2fc592c7ea2a0346)
on `full-captures-upstream`: six product files in one commit on Bloomberg main.
Its [complete diff](https://github.com/jeremycarroll/pytest-memray/compare/92a9c85ccbeba900fd52d59395aae0443a0b13a7...9cb7f4814daf9a50dec0101b2fc592c7ea2a0346)
contains no Symphony client template, planning records or working files.

The preparation commit is App-authored, unsigned and has no DCO signoff.
Jeremy's acceptance is pending; certification and submission remain with
[100-114](https://linear.app/1000lines/issue/100-114) after this PR is accepted,
merged and 100-113 is Done. No upstream PR has been opened.

## Proposed body

Issue number: #160

**Describe your changes**

Add `--memray-full` and `memray_full = true` to retain full allocation captures
for `memray stats` and other allocation-level reporters. Aggregated captures
remain the default. Tracking activation and native/Python allocator tracing
options are unchanged. Documentation explains capture retention and the larger
files and possible runtime overhead of full mode.

**Testing performed**

Regression tests cover CLI/ini parsing, Tracker selection and persisted captures.
Locally: 198 passed, 12 interpreter skips on Python 3.9.25, pytest 8.4.2 and Memray
1.20.0; lint, docs and source/wheel builds passed. A plugin-produced full capture
worked with `memray stats`; the matching aggregated capture was rejected as
expected. All 12 fork CI checks passed, including Python 3.8–3.15.

**Additional context**

Prepared with AI assistance. Development history and detailed validation are
available in [the fork preparation PR](https://github.com/jeremycarroll/pytest-memray/pull/10).
