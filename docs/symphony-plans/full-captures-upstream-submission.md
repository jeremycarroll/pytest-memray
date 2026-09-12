# Full-capture upstream submission

Prepared package for [100-114](https://linear.app/1000lines/issue/100-114).
**Submission is pending.** No upstream PR number or certified replacement head
has been observed. The feature fragment remains `docs/news/160.feature.rst`.

## Contribution and prerequisite

The [six-file contribution](https://github.com/jeremycarroll/pytest-memray/compare/92a9c85ccbeba900fd52d59395aae0443a0b13a7...9cb7f4814daf9a50dec0101b2fc592c7ea2a0346)
adds full allocation captures while preserving the aggregated default.
This task starts from fork `main` at
`f4bccd05ed1ff16db6a234e25ef40d95134b8123`; its PR targets `main`.

[FC-D / PR #10](https://github.com/jeremycarroll/pytest-memray/pull/10) is still
awaiting acceptance and merge. Its proposed preparation record was read at
`9b88772ee77f545bfc5bb6eb5d60ca60d725e69f`, **not an accepted FC-D ref**.
Jeremy must accept the exact artifact, PR #10 must merge to main, and
[100-113](https://linear.app/1000lines/issue/100-113) must be Done before branch
ownership transfers. Refresh all three observations before dependent writes.
No predecessor commits are included in this task branch.

Observed on 2026-09-12:

| Item                                     | Readback                                                                               |
| ---------------------------------------- | -------------------------------------------------------------------------------------- |
| Upstream main / sole artifact parent     | `92a9c85ccbeba900fd52d59395aae0443a0b13a7`                                             |
| Fork `full-captures-upstream` / old head | `9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`                                             |
| Artifact tree                            | `e96ee97305d4c02732e0b2859edc0ce1b99468f3`                                             |
| Author and committer                     | `1000lines-symphony[bot] <326272204+1000lines-symphony[bot]@users.noreply.github.com>` |
| Certification                            | No `Signed-off-by` trailer; unsigned App preparation commit                            |
| Certified replacement / final artifact   | Pending; no SHA assigned                                                               |
| Upstream PR / number / rename            | All-state head query returned `[]`; pending                                            |

The remote matches FC-D's recorded artifact. `git log base..head` contains only
that product commit; the diff is six files, 560 additions and 39 deletions.
The artifact excludes fork-only history and Symphony template, planning and
working files. The detailed inventory remains in the fork's PR #10 history.
The scoped marker audit found no project TODO, stub or temporary adapter in
those six files. Temporary-directory references describe normal capture cleanup
and test fixtures; the full-capture opt-in is an intentional public setting.

## Refreshed upstream sources

Upstream main is unchanged. Its complete tree has no contribution or PR template;
the [organization template](https://github.com/bloomberg/.github/blob/6e6478c5f719f8ac2251558635f700dd5c0f128e/PULL_REQUEST_TEMPLATE.md),
[contribution instructions](https://github.com/bloomberg/.github/blob/6e6478c5f719f8ac2251558635f700dd5c0f128e/CONTRIBUTING.md)
and [DCO](https://github.com/bloomberg/.github/blob/6e6478c5f719f8ac2251558635f700dd5c0f128e/DCO.md)
remain at `6e6478c5f719f8ac2251558635f700dd5c0f128e`.
The README requires real-name signoff for each contribution commit.
Issue #160 and all four comments through `3742617066` were refreshed.

Upstream main is protected; its branch response exposes empty required status
contexts/checks and `/rules/branches/main` returns `[]`. This does not establish
all eventual PR gates. Refresh rules, workflow sources and actual PR checks at
submission, including DCO if emitted or required. A denied required rule read
needs Jeremy's readback before that dependent handoff.

The proposed body follows FC-D's concise revision and
[Jeremy's review](https://github.com/jeremycarroll/pytest-memray/pull/10#pullrequestreview-5187981207),
whose repository admin authority was verified. Merged upstream PRs #107 and
#185 were inspected for presentation. Internal inventories remain in the fork;
the upstream body contains one fork history link.

## Proposed upstream body

Title: **Add opt-in full allocation captures**. Copy only the following body to
`upstream-pr.md` outside the artifact's tracked tree. Its testing paragraph
currently describes the unchanged preparation artifact; refresh check links and
evidence for the accepted certified head before executing submission.

<!-- upstream-body:start -->

_Issue number of the reported bug or feature request: #160_

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
expected. All 12 fork CI checks passed, including Python 3.8–3.15:
[Run](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011559),
[Build](https://github.com/jeremycarroll/pytest-memray/actions/runs/34716011472).

**Additional context**

Prepared with AI assistance. Development history and detailed validation are
available in [the fork preparation PR](https://github.com/jeremycarroll/pytest-memray/pull/10).

<!-- upstream-body:end -->

## Jeremy's certification and submission actions

The runtime author App is `1000lines-symphony` (4866508), bound to fork repository
1366948285 through installation 161167248. Binding that existing App to
`bloomberg/pytest-memray` returned **HTTP 404** on 2026-09-12 (unselected
repository or denied grant, among the broker's possible causes). Its fork grant
does not establish cross-fork submission permission. No credential expansion or
upstream create was attempted. Jeremy performs the following operations in his
own authenticated checkout; no credentials need to be shared with Symphony.

After FC-D acceptance/Done/merge, Jeremy reads the contribution and current DCO,
confirms his right to submit it and verifies his real Git name/email. Under that
identity, the prepared certification operation is:

```shell
gh api user --jq .login
git fetch origin full-captures-upstream
git switch full-captures-upstream
git status --short
git rev-parse HEAD origin/full-captures-upstream
git var GIT_AUTHOR_IDENT
```

The login must be `jeremycarroll`, the working tree clean, and both refs must
still equal the observed old head above. Stop on drift; do not reset unrelated
work. Inspect the sole contribution, then replace only its metadata:

```shell
git commit --amend --signoff --reset-author --no-edit
git show -s --format='%H%n%P%n%T%n%an <%ae>%n%B' HEAD
git log --format=fuller 92a9c85ccbeba900fd52d59395aae0443a0b13a7..HEAD
git diff --exit-code 9cb7f4814daf9a50dec0101b2fc592c7ea2a0346 HEAD
git push --force-with-lease=refs/heads/full-captures-upstream:9cb7f4814daf9a50dec0101b2fc592c7ea2a0346 origin HEAD:refs/heads/full-captures-upstream
git ls-remote origin refs/heads/full-captures-upstream
```

Before push, verify exactly one commit, parent and tree equal the recorded
values, genuine author/signoff, and an empty tree diff. Record the new SHA and
remote readback. Symphony then reruns all 12 artifact checks and obtains fresh
review covering that exact certified head in this main-based task PR. A later
acknowledgement cannot certify an earlier unsigned commit.

Only after those gates pass, refresh `upstream-pr.md` and use Jeremy's account:

```shell
gh api --method GET repos/bloomberg/pytest-memray/pulls -f state=all -f head=jeremycarroll:full-captures-upstream
gh pr create --repo bloomberg/pytest-memray --base main --head jeremycarroll:full-captures-upstream --title "Add opt-in full allocation captures" --body-file upstream-pr.md
```

If an association already exists or create has an ambiguous result, inspect it
before retrying. Jeremy supplies the actual URL; Symphony reads back URL/number,
base `main`, head repository/ref/SHA, author, files, commits/signoffs and checks.
Successful fork push and actual authorized cross-fork creation establish their
respective permissions; upstream collaborator write permission is not required.

## Actual-number rename and final evidence

After recording the observed upstream number N, check for a destination
collision, then rename only `docs/news/160.feature.rst` to
`docs/news/N.feature.rst` on the artifact and task branch, preserving its bytes.
N=160 is an evidence-backed no-op. Jeremy signs off the artifact rename as a
normal descendant commit; the task commit uses the actual worker identity.

Rerun towncrier draft, `make docs` and `git diff --check` on both surfaces, plus
Prettier on this record. Changed upstream/product source also requires artifact
`make check`, `make lint`, build and affected reporter proof. Native mode is
selected by fork-main configuration; there is no Docker override. Use Docker
only for environment gaps, then mandatory current-head CI.

Prior installed provenance is separate: FC-D installed/tested artifact
`9cb7f4814daf9a50dec0101b2fc592c7ea2a0346` noneditably with Python 3.9.25,
pytest 8.4.2 and Memray 1.20.0. FC-C installed/tested
`0b2d99061f49ad125e84577780b01a3a4edcf3e3`; FC-A's minimum Memray 1.19.1 and
object-tracking evidence remains historical. No new artifact install is claimed.

All 12 existing artifact jobs were read back as successful at `9cb7f481`, App
15368, push event, attempt 1 in the linked Run/Build workflows. They cannot stand
in for checks on a later certified or renamed head. Final task/artifact heads
need all 12 baseline jobs; actual upstream requirements must also pass.
Record workflow, run/attempt, App, SHA and each child result in the workpad.

Before final handoff, record accepted FC-D ref, certified/final heads, actual
upstream URL/number, exact rename, current checks and maintainer feedback.
Inspect all review/comment/thread surfaces and fresh Linear feedback. Obtain
fresh Codex/hackcadence approval of the current task head covering the final
artifact, close mandatory feedback and verify a clean, ready task PR with
orange/symphony labels and Jeremy assigned. Until then this package is prepared,
not submitted or accepted. Jeremy owns Done and later maintainer responses;
retain the submission branch while its upstream PR depends on it.
