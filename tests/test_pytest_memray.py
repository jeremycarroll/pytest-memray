from __future__ import annotations

import pickle
import re
import sys
import xml.etree.ElementTree as ET
from types import SimpleNamespace
from unittest.mock import ANY
from unittest.mock import patch

import pytest
from memray import FileFormat
from memray import FileReader
from memray import Tracker
from pytest import ExitCode
from pytest import Pytester

from pytest_memray.marks import StackFrame
from pytest_memray.plugin import Manager


@pytest.fixture(params=[[], ["--memray-full"]], ids=["aggregated", "full"])
def capture_args(request: pytest.FixtureRequest) -> list[str]:
    return request.param


def configure_full_capture(
    pytester: Pytester, config_file: str, value: str | None
) -> None:
    setting = "" if value is None else f"memray_full = {value}"
    if config_file == "pytest.ini":
        pytester.makeini(f"[pytest]\n{setting}")
    else:
        # Exercise native TOML Booleans as well as pytest's string forms.
        if value is not None and value not in ("true", "false"):
            setting = f'memray_full = "{value}"'
        pytester.makepyprojecttoml(f"[tool.pytest.ini_options]\n{setting}")


def extract_stacks(test_output: str) -> list[list[StackFrame]]:
    ret: list[list[StackFrame]] = []
    before_start = True
    for line in test_output.splitlines():
        if before_start:
            if "List of allocations:" in line:
                before_start = False
        elif "allocated here" in line:
            ret.append([])
        elif (match := re.match(r"^ {8}([^:]+):(.*):(\d+)$", line)) is not None:
            ret[-1].append(
                StackFrame(function=match[1], filename=match[2], lineno=int(match[3]))
            )

    return ret


def test_help_message(pytester: Pytester) -> None:
    result = pytester.runpytest("--help")
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "memray:",
            "*--memray*Activate memray tracking",
            "*--memray-full*Capture all allocations*",
            "*memray (bool)*",
            "*memray_full (bool)*",
        ]
    )
    assert "larger files and potentially slower runs" in " ".join(
        result.stdout.str().split()
    )


@pytest.mark.parametrize("config_file", ["pytest.ini", "pyproject.toml"])
@pytest.mark.parametrize(
    "ini, args, full",
    [
        (None, [], False),
        ("false", [], False),
        ("true", [], True),
        ("yes", [], True),
        ("on", [], True),
        ("1", [], True),
        ("TrUe", [], True),
        ("no", [], False),
        ("off", [], False),
        ("0", [], False),
        ("FaLsE", [], False),
        (None, ["--memray-full"], True),
        ("false", ["--memray-full"], True),
        ("true", ["--memray-full"], True),
        ("false", ["--memray-full", "--memray-full"], True),
        ("true", ["--memray-full", "--memray-full"], True),
        ("true", ["-o", "memray_full=false"], False),
        ("false", ["-o", "memray_full=true"], True),
        ("true", ["--memray-full", "-o", "memray_full=false"], True),
    ],
)
def test_full_capture_configuration(
    pytester: Pytester, config_file: str, ini: str | None, args: list[str], full: bool
) -> None:
    configure_full_capture(pytester, config_file, ini)
    pytester.makepyfile("def test_allocates():\n    assert bytearray(4096)")

    with patch("pytest_memray.plugin.Tracker", wraps=Tracker) as tracker:
        result = pytester.runpytest("--memray", *args)

    result.assert_outcomes(passed=1)
    tracker.assert_called_once_with(
        ANY,
        native_traces=False,
        trace_python_allocators=False,
        file_format=(
            FileFormat.ALL_ALLOCATIONS if full else FileFormat.AGGREGATED_ALLOCATIONS
        ),
    )


@pytest.mark.parametrize("config_file", ["pytest.ini", "pyproject.toml"])
@pytest.mark.parametrize("active", [False, True])
@pytest.mark.parametrize("persistent", [False, True])
def test_invalid_full_capture_ini_fails_before_setup(
    pytester: Pytester,
    monkeypatch: pytest.MonkeyPatch,
    config_file: str,
    active: bool,
    persistent: bool,
    capture_args: list[str],
) -> None:
    monkeypatch.delenv("MEMRAY_RESULT_PATH", raising=False)
    configure_full_capture(pytester, config_file, "sometimes")
    pytester.makepyfile("def test_not_run():\n    assert False")
    dump = pytester.path / "captures"
    args = ["--memray"] if active else []
    if persistent:
        # The existing argument parser creates this directory; Manager must
        # never create its metadata directory or temporary result directory.
        args.extend(["--memray-bin-path", str(dump)])

    with patch("pytest_memray.plugin.Manager", wraps=Manager) as manager:
        with patch("pytest_memray.plugin.Tracker") as tracker:
            with patch("pytest_memray.plugin.TemporaryDirectory") as temporary:
                result = pytester.runpytest(*args, *capture_args)

    assert result.ret == ExitCode.USAGE_ERROR
    result.stderr.fnmatch_lines(["*memray_full*sometimes*"])
    manager.assert_not_called()
    tracker.assert_not_called()
    temporary.assert_not_called()
    assert not (dump / "metadata").exists()
    assert not list(dump.glob("*.bin"))


@pytest.mark.parametrize("config_file", ["pytest.ini", "pyproject.toml"])
@pytest.mark.parametrize("value", ["false", "true", "sometimes"])
def test_full_capture_flag_rejects_attached_values(
    pytester: Pytester, config_file: str, value: str
) -> None:
    configure_full_capture(pytester, config_file, "true")
    with patch("pytest_memray.plugin.Manager") as manager:
        result = pytester.runpytest(f"--memray-full={value}")

    assert result.ret == ExitCode.USAGE_ERROR
    result.stderr.fnmatch_lines(["*--memray-full*ignored explicit argument*"])
    manager.assert_not_called()


@pytest.mark.parametrize("config_file", ["pytest.ini", "pyproject.toml"])
@pytest.mark.parametrize("marked", [False, True])
def test_full_capture_ini_preserves_activation(
    pytester: Pytester, config_file: str, marked: bool
) -> None:
    configure_full_capture(pytester, config_file, "true")
    marker = '@pytest.mark.limit_memory("1MB")' if marked else ""
    pytester.makepyfile(
        f"import pytest\n{marker}\ndef test_allocates():\n    assert bytearray(4096)"
    )
    with patch("pytest_memray.plugin.Tracker", wraps=Tracker) as tracker:
        result = pytester.runpytest()

    result.assert_outcomes(passed=1)
    assert "MEMRAY REPORT" not in result.stdout.str()
    if marked:
        tracker.assert_called_once_with(
            ANY,
            native_traces=False,
            trace_python_allocators=False,
            file_format=FileFormat.ALL_ALLOCATIONS,
        )
    else:
        tracker.assert_not_called()


def test_memray_is_called_when_activated(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        def test_hello_world():
            assert 2 == 1 + 1
    """
    )

    with patch("pytest_memray.plugin.Tracker") as mock:
        result = pytester.runpytest("--memray")

    mock.assert_called_once()
    assert result.ret == ExitCode.OK


def test_memray_is_not_called_when_not_activated(
    pytester: Pytester, capture_args: list[str]
) -> None:
    pytester.makepyfile(
        """
        def test_hello_world():
            assert 2 == 1 + 1
    """
    )

    with patch("pytest_memray.plugin.Tracker") as mock:
        result = pytester.runpytest(*capture_args)

    mock.assert_not_called()
    assert result.ret == ExitCode.OK


@pytest.mark.parametrize(
    "size, outcome",
    [
        (1024 * 5, ExitCode.TESTS_FAILED),
        (1024 * 2, ExitCode.TESTS_FAILED),
        (1024 * 2 - 1, ExitCode.OK),
        (1024 * 1, ExitCode.OK),
    ],
)
def test_limit_memory_marker(
    pytester: Pytester, size: int, outcome: ExitCode, capture_args: list[str]
) -> None:
    pytester.makepyfile(
        f"""
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("2KB")
        def test_memory_alloc_fails():
            allocator.valloc({size})
            allocator.free()
        """
    )

    result = pytester.runpytest(*capture_args, "--memray")

    assert result.ret == outcome


def test_limit_memory_marker_does_work_if_memray_not_passed(
    pytester: Pytester, capture_args: list[str]
) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("2KB")
        def test_memory_alloc_fails():
            allocator.valloc(4*1024)
            allocator.free()
        """
    )

    result = pytester.runpytest(*capture_args)

    assert result.ret == ExitCode.TESTS_FAILED


@pytest.mark.parametrize(
    "memlimit, mem_to_alloc",
    [(5, 100), (10, 200)],
)
def test_memray_with_junit_xml_error_msg(
    pytester: Pytester, memlimit: int, mem_to_alloc: int
):
    xml_output_file = pytester.makefile(".xml", "")
    pytester.makepyfile(
        f"""
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("{memlimit}B")
        def test_memory_alloc_fails():
            allocator.valloc({mem_to_alloc})
            allocator.free()
        """
    )
    result = pytester.runpytest("--memray", "--junit-xml", xml_output_file)
    assert result.ret == ExitCode.TESTS_FAILED

    expected = f"Test was limited to {memlimit}.0B but allocated {mem_to_alloc}.0B"
    root = ET.parse(str(xml_output_file)).getroot()
    for testcase in root.iter("testcase"):
        failure = testcase.find("failure")
        assert expected in failure.text


def test_memray_with_junit_xml(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("1B")
        def test_memory_alloc_fails():
            allocator.valloc(1234)
            allocator.free()
        """
    )
    path = str(pytester.path / "blech.xml")
    result = pytester.runpytest("--memray", "--junit-xml", path)
    assert result.ret == ExitCode.TESTS_FAILED


@pytest.mark.parametrize("num_stacks", [1, 5, 100])
def test_memray_report_limit_number_stacks(num_stacks: int, pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        def rec(n):
            if n <= 1:
                allocator.valloc(1024*2)
                allocator.free()
                return None
            return rec(n - 1)


        @pytest.mark.limit_memory("1kb")
        def test_foo():
            rec(10)
    """
    )

    result = pytester.runpytest("--memray", f"--stacks={num_stacks}")

    assert result.ret == ExitCode.TESTS_FAILED

    stacks = extract_stacks(result.stdout.str())
    valloc_stacks = [stack for stack in stacks if stack[0].function == "valloc"]
    (valloc_stack,) = valloc_stacks
    num_rec_frames = sum(1 for frame in valloc_stack if frame.function == "rec")
    assert num_rec_frames == min(num_stacks - 1, 10)


@pytest.mark.parametrize(
    "extra_args, expect_allocations",
    [
        (["-q"], False),
        ([], True),
        (["-v"], True),
        (["-vv"], True),
        (["-vvv"], True),
        (["-o", "verbosity_memray=2"], True),
        (["-vv", "-o", "verbosity_memray=-1"], False),
    ],
)
def test_limit_memory_allocation_list_visibility(
    pytester: Pytester, extra_args: list[str], expect_allocations: bool
) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("1KB")
        def test_foo():
            allocator.valloc(1024 * 4)
            allocator.free()
        """
    )

    result = pytester.runpytest("--memray", *extra_args)
    assert result.ret == ExitCode.TESTS_FAILED
    stacks = extract_stacks(result.stdout.str())
    assert bool(stacks) is expect_allocations


@pytest.mark.parametrize(
    "extra_args, expect_all",
    [
        ([], False),
        (["-v"], False),
        (["-vv"], True),
    ],
)
def test_limit_memory_allocation_list_truncation(
    pytester: Pytester, extra_args: list[str], expect_all: bool
) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator

        def rec(n, allocators):
            a = MemoryAllocator()
            a.valloc(1024)
            allocators.append(a)
            if n > 1:
                rec(n - 1, allocators)

        @pytest.mark.limit_memory("1KB")
        def test_foo():
            allocators = []
            rec(15, allocators)
            for a in allocators:
                a.free()
        """
    )

    result = pytester.runpytest(*extra_args)
    assert result.ret == ExitCode.TESTS_FAILED
    output = result.stdout.str()
    stacks = extract_stacks(output)
    if expect_all:
        assert len(stacks) > 10
        assert "...and" not in output
    else:
        assert len(stacks) == 10
        assert "...and" in output


@pytest.mark.parametrize("native", [True, False])
@pytest.mark.parametrize("trace_python_allocators", [True, False])
def test_memray_report_native(
    native: bool,
    trace_python_allocators: bool,
    pytester: Pytester,
    capture_args: list[str],
) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("1kb")
        def test_foo():
            allocator.valloc(1024*2)
            allocator.free()
    """
    )

    with patch("pytest_memray.plugin.Tracker", wraps=Tracker) as mock:
        result = pytester.runpytest(
            *capture_args,
            "--memray",
            *(["--native"] if native else []),
            *(["--trace-python-allocators"] if trace_python_allocators else []),
        )

    assert result.ret == ExitCode.TESTS_FAILED

    output = result.stdout.str()
    mock.assert_called_once_with(
        ANY,
        native_traces=native,
        trace_python_allocators=trace_python_allocators,
        file_format=(
            FileFormat.ALL_ALLOCATIONS
            if capture_args
            else FileFormat.AGGREGATED_ALLOCATIONS
        ),
    )

    if native:
        assert "MemoryAllocator_" in output
    else:
        assert "MemoryAllocator_" not in output


@pytest.mark.parametrize("trace_python_allocators", [True, False])
def test_memray_report_python_allocators(
    trace_python_allocators: bool, pytester: Pytester, capture_args: list[str]
) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import PymallocMemoryAllocator
        from memray._test import PymallocDomain

        allocator = PymallocMemoryAllocator(PymallocDomain.PYMALLOC_OBJECT)

        def allocate_with_pymalloc():
            allocator.malloc(256)
            allocator.free()

        @pytest.mark.limit_memory("128B")
        def test_foo():
            allocate_with_pymalloc()
    """
    )

    with patch("pytest_memray.plugin.Tracker", wraps=Tracker) as mock:
        result = pytester.runpytest(
            *capture_args,
            "--memray",
            *(["--trace-python-allocators"] if trace_python_allocators else []),
        )

    assert result.ret == (
        ExitCode.TESTS_FAILED if trace_python_allocators else ExitCode.OK
    )

    output = result.stdout.str()
    mock.assert_called_once_with(
        ANY,
        native_traces=False,
        trace_python_allocators=trace_python_allocators,
        file_format=(
            FileFormat.ALL_ALLOCATIONS
            if capture_args
            else FileFormat.AGGREGATED_ALLOCATIONS
        ),
    )

    if trace_python_allocators:
        assert "allocate_with_pymalloc" in output
    else:
        assert "allocate_with_pymalloc" not in output


def test_memray_report(pytester: Pytester, capture_args: list[str]) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        def allocating_func1():
            allocator.valloc(1024)
            allocator.free()

        def allocating_func2():
            allocator.valloc(1024*2)
            allocator.free()

        def test_foo():
            allocating_func1()

        def test_bar():
            allocating_func2()
        """
    )

    result = pytester.runpytest(*capture_args, "--memray")

    assert result.ret == ExitCode.OK

    output = result.stdout.str()

    assert "MEMRAY REPORT" in output

    assert "results for test_memray_report.py::test_foo" in output
    assert "Total memory allocated: 2.0KiB" in output
    assert "valloc:" in output
    assert "-> 2.0KiB" in output

    assert "results for test_memray_report.py::test_bar" in output
    assert "Total memory allocated: 1.0KiB" in output
    assert "valloc:" in output
    assert "-> 1.0KiB" in output


def test_memray_report_is_not_shown_if_deactivated(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        def allocating_func1():
            allocator.valloc(1024)
            allocator.free()

        def allocating_func2():
            allocator.valloc(1024*2)
            allocator.free()

        def test_foo():
            allocating_func1()

        def test_bar():
            allocating_func2()
        """
    )

    result = pytester.runpytest("--memray", "--hide-memray-summary")

    assert result.ret == ExitCode.OK

    output = result.stdout.str()

    assert "MEMRAY REPORT" not in output

    assert "results for test_memray_report.py::test_foo" not in output
    assert "Total memory allocated: 2.0KiB" not in output
    assert "valloc:" not in output
    assert "-> 2.0KiB" not in output

    assert "results for test_memray_report.py::test_bar" not in output
    assert "Total memory allocated: 1.0KiB" not in output
    assert "valloc:" not in output
    assert "-> 1.0KiB" not in output


def test_memray_report_limit(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        def allocating_func1():
            allocator.valloc(1024*1024)
            allocator.free()

        def allocating_func2():
            allocator.valloc(1024*1024*2)
            allocator.free()

        def test_foo():
            allocating_func1()

        def test_bar():
            allocating_func2()
    """
    )

    result = pytester.runpytest("--memray", "--most-allocations=1")

    assert result.ret == ExitCode.OK

    output = result.stdout.str()

    assert "results for test_memray_report_limit.py::test_foo" not in output
    assert "results for test_memray_report_limit.py::test_bar" in output


def test_memray_report_limit_without_limit(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        def allocating_func1():
            allocator.valloc(1024)
            allocator.free()

        def allocating_func2():
            allocator.valloc(1024*2)
            allocator.free()

        def test_foo():
            allocating_func1()

        def test_bar():
            allocating_func2()
    """
    )

    result = pytester.runpytest("--memray", "--most-allocations=0")

    assert result.ret == ExitCode.OK

    output = result.stdout.str()

    assert "results for test_memray_report_limit_without_limit.py::test_foo" in output
    assert "results for test_memray_report_limit_without_limit.py::test_bar" in output


def test_failing_tests_are_not_reported(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        def allocating_func1():
            allocator.valloc(1024)
            allocator.free()

        def allocating_func2():
            allocator.valloc(1024*2)
            allocator.free()

        def test_foo():
            allocating_func1()

        def test_bar():
            allocating_func2()
            1/0
        """
    )

    result = pytester.runpytest("--memray")

    assert result.ret == ExitCode.TESTS_FAILED

    output = result.stdout.str()

    assert "results for test_failing_tests_are_not_reported.py::test_foo" in output
    assert "results for test_failing_tests_are_not_reported.py::test_bar" not in output


def test_plugin_calls_tests_only_once(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        counter = 0
        def test_hello_world():
            global counter
            counter += 1
            assert counter < 2
        """
    )

    with patch("pytest_memray.plugin.Tracker") as mock:
        result = pytester.runpytest("--memray")

    mock.assert_called_once()
    assert result.ret == ExitCode.OK


def test_bin_path(pytester: Pytester) -> None:
    py = """
    import pytest

    def test_a():
        assert [1]
    @pytest.mark.parametrize('i', [1, 2])
    def test_b(i):
        assert [2] * i
    """
    pytester.makepyfile(**{"magic/test_a": py})
    dump = pytester.path / "d"
    with patch("uuid.uuid4", return_value=SimpleNamespace(hex="H")) as mock:
        result = pytester.runpytest("--memray", "--memray-bin-path", str(dump))

    assert result.ret == ExitCode.OK
    mock.assert_called_once()

    assert dump.exists()
    assert {i.name for i in dump.iterdir()} == {
        "H-magic-test_a.py-test_b[2].bin",
        "H-magic-test_a.py-test_a.bin",
        "H-magic-test_a.py-test_b[1].bin",
        "metadata",
    }

    output = result.stdout.str()
    assert f"Created 3 binary dumps at {dump} with prefix H" in output


@pytest.mark.parametrize("prefix", [None, "capture"])
def test_persisted_captures_are_readable_after_exit(
    pytester: Pytester,
    monkeypatch: pytest.MonkeyPatch,
    capture_args: list[str],
    prefix: str | None,
) -> None:
    monkeypatch.delenv("MEMRAY_RESULT_PATH", raising=False)
    pytester.makepyfile(
        **{
            "magic/test_allocations": """
                import pytest

                def test_single():
                    assert bytearray(4096)

                @pytest.mark.parametrize('size', [8192, 16384])
                def test_parameter(size):
                    assert bytearray(size)
            """
        }
    )
    dump = pytester.path / "captures"
    prefix_args = ["--memray-bin-prefix", prefix] if prefix is not None else []
    result = pytester.runpytest_subprocess(
        "--memray", *capture_args, "--memray-bin-path", str(dump), *prefix_args
    )
    result.assert_outcomes(passed=3)

    captures = sorted(dump.glob("*.bin"))
    assert len(captures) == 3
    emitted_prefix = captures[0].name.split("-", 1)[0]
    if prefix is None:
        assert re.fullmatch(r"[0-9a-f]{32}", emitted_prefix)
    else:
        assert emitted_prefix == prefix
    cases = {"test_single", "test_parameter[8192]", "test_parameter[16384]"}
    assert {path.name for path in captures} == {
        f"{emitted_prefix}-magic-test_allocations.py-{case}.bin" for case in cases
    }
    metadata_files = list((dump / "metadata").glob("*.metadata"))
    assert {path.stem for path in metadata_files} == {path.stem for path in captures}
    results = [pickle.loads(path.read_bytes()) for path in metadata_files]
    assert {item.test_id for item in results} == {
        f"magic/test_allocations.py::{case}" for case in cases
    }
    for item in results:
        assert item.result_file in captures
        assert item.result_file.stat().st_size > 0
        with FileReader(item.result_file) as reader:
            assert reader.metadata == item.metadata
            assert reader.metadata.file_format == (
                FileFormat.ALL_ALLOCATIONS
                if capture_args
                else FileFormat.AGGREGATED_ALLOCATIONS
            )
            assert reader.metadata.peak_memory > 0
            assert reader.metadata.total_allocations > 0
            assert not reader.metadata.has_native_traces
            assert not reader.metadata.trace_python_allocators
            assert list(reader.get_high_watermark_allocation_records())
        assert reader.closed
        assert item.result_file.exists()


def test_stats_requires_full_capture(
    pytester: Pytester, monkeypatch: pytest.MonkeyPatch, capture_args: list[str]
) -> None:
    monkeypatch.delenv("MEMRAY_RESULT_PATH", raising=False)
    test_file = pytester.makepyfile(
        """
        def test_allocations():
            buffers = [bytearray(4096) for _ in range(20)]
            assert sum(map(len, buffers)) == 81920
        """
    )
    dump = pytester.path / "captures"
    result = pytester.runpytest_subprocess(
        "--memray", *capture_args, "--memray-bin-path", str(dump), str(test_file)
    )
    result.assert_outcomes(passed=1)
    (capture,) = dump.glob("*.bin")
    stats = pytester.run(sys.executable, "-m", "memray", "stats", str(capture))

    if capture_args:
        assert stats.ret == 0
        match = re.search(r"Total allocations:\s*([\d,]+)", stats.stdout.str())
        assert match is not None
        assert int(match[1].replace(",", "")) > 0
    else:
        assert stats.ret != 0
        assert "pre-aggregated capture file" in stats.stderr.str()


@pytest.mark.parametrize("source", ["cli", "pytest.ini", "pyproject.toml"])
def test_full_capture_propagates_to_workers(
    pytester: Pytester, monkeypatch: pytest.MonkeyPatch, source: str
) -> None:
    monkeypatch.delenv("MEMRAY_RESULT_PATH", raising=False)
    args = ["--memray-full"] if source == "cli" else []
    if source != "cli":
        configure_full_capture(pytester, source, "true")
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.parametrize('size', [4096, 8192])
        def test_allocations(size):
            assert bytearray(size)
        """
    )
    dump = pytester.path / "captures"
    result = pytester.runpytest_subprocess(
        "--memray", *args, "-n", "2", "--memray-bin-path", str(dump)
    )
    result.assert_outcomes(passed=2)
    assert "MEMRAY REPORT" in result.stdout.str()
    assert "Total memory allocated:" in result.stdout.str()
    captures = list(dump.glob("*.bin"))
    assert len(captures) == 2
    for capture in captures:
        with FileReader(capture) as reader:
            assert reader.metadata.file_format == FileFormat.ALL_ALLOCATIONS
            assert reader.metadata.peak_memory > 0


def test_temporary_full_captures_are_cleaned_up(
    pytester: Pytester, monkeypatch: pytest.MonkeyPatch, capture_args: list[str]
) -> None:
    monkeypatch.delenv("MEMRAY_RESULT_PATH", raising=False)
    pytester.makepyfile("def test_allocates():\n    assert bytearray(4096)")
    with patch("pytest_memray.plugin.Tracker", wraps=Tracker) as tracker:
        result = pytester.runpytest("--memray", *capture_args)
    result.assert_outcomes(passed=1)
    tracker.assert_called_once()
    capture = tracker.call_args.args[0]
    assert not capture.exists()
    assert not capture.parent.exists()


def test_bin_path_with_long_test_id(
    pytester: Pytester, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("MEMRAY_RESULT_PATH", raising=False)
    py = """
    import pytest

    @pytest.mark.parametrize('v', ['a' * 300])
    def test_a(v):
        assert [1]
    """
    pytester.makepyfile(**{"test_a": py})
    dump = pytester.path / "d"
    result = pytester.runpytest_subprocess(
        "--memray",
        "--memray-bin-path",
        str(dump),
        "--memray-bin-prefix",
        "352f3f34aa644bc2b3672ef467430223",
    )

    assert result.ret == ExitCode.OK

    expected_stem = (
        "352f3f34aa644bc2b3672ef467430223"
        + "-test_a.py-test_a["
        + ("a" * 179)
        + "-88c716620b48351a"
    )

    dumps = [i.name for i in dump.iterdir() if i.name != "metadata"]
    assert len(dumps) == 1
    assert dumps[0] == f"{expected_stem}.bin"
    metadata = list((dump / "metadata").iterdir())
    assert len(metadata) == 1
    assert metadata[0].name == f"{expected_stem}.metadata"
    assert len(metadata[0].name.encode("utf-8")) == 255


def test_bin_path_with_long_test_id_and_long_prefix(
    pytester: Pytester, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("MEMRAY_RESULT_PATH", raising=False)
    py = """
    import pytest

    @pytest.mark.parametrize('v', ['a' * 300])
    def test_a(v):
        assert [1]
    """
    pytester.makepyfile(**{"test_a": py})
    dump = pytester.path / "d"
    result = pytester.runpytest_subprocess(
        "--memray",
        "--memray-bin-path",
        str(dump),
        "--memray-bin-prefix",
        "352f3f34aa644bc2b3672ef467430223" * 3,
    )

    assert result.ret == ExitCode.OK

    expected_stem = (
        ("352f3f34aa644bc2b3672ef467430223" * 3)
        + "-test_a.py-test_a["
        + ("a" * 115)
        + "-3e4fe15eabd37073"
    )

    dumps = [i.name for i in dump.iterdir() if i.name != "metadata"]
    assert len(dumps) == 1
    assert dumps[0] == f"{expected_stem}.bin"
    metadata = list((dump / "metadata").iterdir())
    assert len(metadata) == 1
    assert metadata[0].name == f"{expected_stem}.metadata"
    assert len(metadata[0].name.encode("utf-8")) == 255


@pytest.mark.parametrize("override", [True, False])
def test_bin_path_prefix(
    pytester: Pytester, override: bool, capture_args: list[str]
) -> None:
    py = """
    import pytest
    def test_t():
        assert [1]
    """
    pytester.makepyfile(test_a=py)

    bin_path = pytester.path / "p-test_a.py-test_t.bin"
    if override:
        bin_path.write_bytes(b"")

    args = [*capture_args, "--memray", "--memray-bin-path", str(pytester.path)]
    args.extend(["--memray-bin-prefix", "p"])
    result = pytester.runpytest(*args)
    res = list(pytester.path.iterdir())

    assert res

    assert result.ret == ExitCode.OK
    assert bin_path.exists()


def test_plugin_works_with_the_flaky_plugin(
    pytester: Pytester, capture_args: list[str]
) -> None:
    pytester.makepyfile(
        """
        from flaky import flaky

        @flaky
        def test_hello_world():
            1/0
        """
    )

    with patch("pytest_memray.plugin.Tracker") as mock:
        result = pytester.runpytest(*capture_args, "--memray")

    # Ensure that flaky has only called our Tracker once per retry (2 times)
    # and not more times because it has incorrectly wrapped our plugin and
    # called it multiple times per retry.
    assert mock.call_count == 2
    assert result.ret == ExitCode.TESTS_FAILED


def test_memray_report_with_pytest_xdist(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        def allocating_func1():
            allocator.valloc(1024)
            allocator.free()

        def allocating_func2():
            allocator.valloc(1024*2)
            allocator.free()

        @pytest.mark.parametrize("param", [("unused",)], ids=["x" * 1024])
        def test_foo(param):
            allocating_func1()

        def test_bar():
            allocating_func2()
        """
    )

    result = pytester.runpytest("--memray", "-n", "2")

    assert result.ret == ExitCode.OK

    output = result.stdout.str()

    assert "MEMRAY REPORT" in output

    # We don't check the exact number of memory allocated because pytest-xdist
    # can spawn some threads using the `execnet` library which can allocate extra
    # memory.
    assert "Total memory allocated:" in output

    assert "results for test_memray_report_with_pytest_xdist.py::test_foo" in output
    assert "valloc:" in output
    assert "-> 2.0KiB" in output

    assert "results for test_memray_report_with_pytest_xdist.py::test_bar" in output
    assert "valloc:" in output
    assert "-> 1.0KiB" in output


@pytest.mark.parametrize(
    "size, outcome",
    [
        (1024 * 20, ExitCode.TESTS_FAILED),
        (1024 * 10, ExitCode.TESTS_FAILED),
        (1024, ExitCode.OK),
    ],
)
def test_limit_memory_marker_with_pytest_xdist(
    pytester: Pytester, size: int, outcome: ExitCode
) -> None:
    pytester.makepyfile(
        f"""
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("10KB")
        def test_memory_alloc_fails():
            allocator.valloc({size})
            allocator.free()

        @pytest.mark.limit_memory("10KB")
        def test_memory_alloc_fails_2():
            allocator.valloc({size})
            allocator.free()
        """
    )

    result = pytester.runpytest("--memray", "-n", "2")
    assert result.ret == outcome


def test_memray_does_not_raise_warnings(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("1MB")
        def test_memory_alloc_fails():
            allocator.valloc(1234)
            allocator.free()
        """
    )
    result = pytester.runpytest("-Werror", "--memray")
    assert result.ret == ExitCode.OK


@pytest.mark.parametrize(
    "size, outcome",
    [
        (0, ExitCode.OK),
        (1, ExitCode.OK),
        (1024 * 1 / 10, ExitCode.OK),
        (1024 * 1, ExitCode.TESTS_FAILED),
        (1024 * 10, ExitCode.TESTS_FAILED),
    ],
)
def test_leak_marker(
    pytester: Pytester, size: int, outcome: ExitCode, capture_args: list[str]
) -> None:
    pytester.makepyfile(
        f"""
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()
        @pytest.mark.limit_leaks("5KB")
        def test_memory_alloc_fails():
            for _ in range(10):
                allocator.valloc({size})
                # No free call here
        """
    )

    with patch("pytest_memray.plugin.Tracker", wraps=Tracker) as tracker:
        result = pytester.runpytest(*capture_args, "--memray")

    tracker.assert_called_once_with(
        ANY,
        native_traces=True,
        trace_python_allocators=True,
        file_format=(
            FileFormat.ALL_ALLOCATIONS
            if capture_args
            else FileFormat.AGGREGATED_ALLOCATIONS
        ),
    )

    assert result.ret == outcome


@pytest.mark.parametrize(
    "size, outcome",
    [
        (4 * 1024, ExitCode.OK),
        (0.4 * 1024 * 1024, ExitCode.OK),
        (4 * 1024 * 1024, ExitCode.TESTS_FAILED),
    ],
)
def test_leak_marker_in_a_thread(
    pytester: Pytester, size: int, outcome: ExitCode
) -> None:
    pytester.makepyfile(
        f"""
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()
        import threading
        def allocating_func():
            for _ in range(10):
                allocator.valloc({size})
                # No free call here
        @pytest.mark.limit_leaks("20MB")
        def test_memory_alloc_fails():
            t = threading.Thread(target=allocating_func)
            t.start()
            t.join()
        """
    )

    result = pytester.runpytest("--memray")
    assert result.ret == outcome


def test_leak_marker_filtering_function(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        LEAK_SIZE = 1024
        allocator = MemoryAllocator()

        def this_should_not_be_there():
            allocator.valloc(LEAK_SIZE)
            # No free call here

        def filtering_function(stack):
            for frame in stack.frames:
                if frame.function == "this_should_not_be_there":
                    return False
            return True

        @pytest.mark.limit_leaks("5KB", filter_fn=filtering_function)
        def test_memory_alloc_fails():
            for _ in range(10):
                this_should_not_be_there()
        """
    )

    result = pytester.runpytest("--memray")

    assert result.ret == ExitCode.OK


def test_leak_marker_does_work_if_memray_not_passed(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()
        @pytest.mark.limit_leaks("0B")
        def test_memory_alloc_fails():
            allocator.valloc(512)
            # No free call here
        """
    )

    result = pytester.runpytest()

    assert result.ret == ExitCode.TESTS_FAILED


def test_multiple_markers_are_not_supported(
    pytester: Pytester, capture_args: list[str]
) -> None:
    pytester.makepyfile(
        """
        import pytest
        @pytest.mark.limit_leaks("0MB")
        @pytest.mark.limit_memory("0MB")
        def test_bar():
            pass
        """
    )

    result = pytester.runpytest(*capture_args, "--memray")
    assert result.ret == ExitCode.TESTS_FAILED

    output = result.stdout.str()
    assert "Only one Memray marker can be applied to each test" in output


def test_multiple_markers_are_not_supported_with_global_marker(
    pytester: Pytester,
) -> None:
    pytester.makepyfile(
        """
        import pytest
        pytestmark = pytest.mark.limit_memory("1 MB")
        @pytest.mark.limit_leaks("0MB")
        def test_bar():
            pass
        """
    )

    result = pytester.runpytest("--memray")
    assert result.ret == ExitCode.TESTS_FAILED

    output = result.stdout.str()
    assert "Only one Memray marker can be applied to each test" in output


def test_fail_on_increase(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("100MB")
        def test_memory_alloc_fails():
            allocator.valloc(1024)
            allocator.free()
        """
    )
    result = pytester.runpytest("--memray")
    assert result.ret == ExitCode.OK
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("100MB")
        def test_memory_alloc_fails():
            allocator.valloc(1024 * 10)
            allocator.free()
        """
    )
    result = pytester.runpytest("--memray", "--fail-on-increase")
    assert result.ret == ExitCode.TESTS_FAILED
    output = result.stdout.str()
    assert "Test uses more memory than previous run" in output
    assert "Test previously used 1.0KiB but now uses 10.0KiB" in output


def test_fail_on_increase_unset(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("100MB")
        def test_memory_alloc_fails():
            allocator.valloc(1024)
            allocator.free()
        """
    )
    result = pytester.runpytest("--memray")
    assert result.ret == ExitCode.OK
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.mark.limit_memory("100MB")
        def test_memory_alloc_fails():
            allocator.valloc(1024 * 10)
            allocator.free()
        """
    )
    result = pytester.runpytest("--memray")
    assert result.ret == ExitCode.OK


def test_limit_memory_in_current_thread(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()
        import threading
        def allocating_func():
            for _ in range(10):
                allocator.valloc(1024*5)
                # No free call here

        @pytest.mark.limit_memory("5KB", current_thread_only=True)
        def test_memory_alloc_fails():
            t = threading.Thread(target=allocating_func)
            t.start()
            t.join()
        """
    )

    result = pytester.runpytest("--memray")

    assert result.ret == ExitCode.OK


def test_leaks_in_current_thread(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()
        import threading
        def allocating_func():
            for _ in range(10):
                allocator.valloc(1024*5)
                # No free call here

        @pytest.mark.limit_leaks("5KB", current_thread_only=True)
        def test_memory_alloc_fails():
            t = threading.Thread(target=allocating_func)
            t.start()
            t.join()
        """
    )

    result = pytester.runpytest("--memray")

    assert result.ret == ExitCode.OK


def test_running_async_tests_with_anyio(
    pytester: Pytester, capture_args: list[str]
) -> None:
    xml_output_file = pytester.makefile(".xml", "")
    pytester.makepyfile(
        """
        import pytest
        from memray._test import MemoryAllocator
        allocator = MemoryAllocator()

        @pytest.fixture
        def anyio_backend():
            return 'asyncio'

        @pytest.mark.limit_leaks("5KB")
        @pytest.mark.anyio
        async def test_memory_alloc_fails():
            for _ in range(10):
                allocator.valloc(1024*10)
                # No free call here
        """
    )

    result = pytester.runpytest(*capture_args, "--junit-xml", xml_output_file)

    assert result.ret != ExitCode.OK

    root = ET.parse(str(xml_output_file)).getroot()
    for testcase in root.iter("testcase"):
        failure = testcase.find("failure")
        assert failure.text == (
            "Test was allowed to leak 5.0KiB per location"
            " but at least one location leaked more"
        )
