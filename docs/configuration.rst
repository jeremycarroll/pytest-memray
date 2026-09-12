Configuration
=============

This plugin provides a clean minimal set of command line options that are added to pytest.
You can also specify most options in ``pytest.ini`` file.
The complete list of command line options is:

.. tab:: Command line options

  ``--memray``
    Activate memray tracking.

  ``--memray-full``
    Use full allocation captures instead of the aggregated default. Produces larger
    files and may add runtime overhead. Does not activate tracking; takes no value.

  ``--most-allocations=MOST_ALLOCATIONS``
    Show the N tests that allocate most memory (N=0 for all).

  ``--hide-memray-summary``
    Hide the memray summary at the end of the execution.

  ``--memray-bin-path``
    Path where to write the memray binary dumps (by default a temporary folder).

  ``--memray-bin-prefix``
    Prefix to use for the binary dump (by default a random UUID4 hex)

  ``--stacks=STACKS``
    Show the N most recent stack entries when showing tracebacks of memory allocations

  ``--native``
    Include native frames when showing tracebacks of memory allocations (will be slower)

  ``--trace-python-allocators``
    Record allocations made by the Pymalloc allocator (will be slower)
  
  ``--fail-on-increase``
    Fail a test with the limit_memory marker if it uses more memory than its last successful run

.. tab:: Config file options

  ``memray(bool)``
    Activate memray tracking.

  ``memray_full(bool)``
    Use full allocation captures (default: false, meaning aggregated captures).
    ``--memray-full`` takes precedence. Does not activate tracking.

  ``most_allocations(int)``
    Show the N tests that allocate most memory (N=0 for all, default=5).

  ``hide_memray_summary(bool)``
    Hide the memray summary at the end of the execution.

  ``stacks(int)``
    Show the N most recent stack entries when showing tracebacks of memory allocations

  ``native(bool)``
    Include native frames when showing tracebacks of memory allocations (will be slower)

  ``trace_python_allocators(bool)``
    Record allocations made by the Pymalloc allocator (will be slower)

  ``fail-on-increase(bool)``
    Fail a test with the limit_memory marker if it uses more memory than its last successful run

  ``verbosity_memray(string)``
    Verbosity level for limit_memory failure reports.
    At negative levels the limit_memory marker only reports a summary,
    at level 0 or 1 it shows the top 10 allocations by size,
    from level 2 up it shows all allocations. The default follows pytest's
    -v / -q flags (with 0 as the default if neither are given).

Full captures and downstream reporters
--------------------------------------

Aggregated captures are the default to reduce disk usage. Full captures retain
individual allocation records for reporters such as `Memray stats
<https://bloomberg.github.io/memray/stats.html>`_ and `temporal flame graphs
<https://bloomberg.github.io/memray/flamegraph.html#temporal-flame-graphs>`_.
Full captures are larger and may increase runtime overhead.

To enable tracking, select full captures and retain them after pytest exits:

.. code-block:: shell

   python -m pytest --memray --memray-full --native --trace-python-allocators \
     --memray-bin-path .memray tests/
   find .memray -type f -name '*.bin'

After pytest exits, select the listed ``.bin`` for the test you want to inspect.
Use that actual path in place of ``CAPTURE.bin`` below; do not select a metadata
file or assume a generated filename prefix:

.. code-block:: shell

   python -m memray stats CAPTURE.bin

The stats reporter needs full allocation data; it cannot compute statistics from
an aggregated capture. Both formats use ``.bin`` filenames, so the extension
does not identify the format. Use a separate output directory for each run when
comparing formats or test configurations, to keep their captures distinct.

Configuration and overrides
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To opt in through ``pytest.ini``:

.. code-block:: ini

   [pytest]
   memray_full = true

Alternatively, use ``pyproject.toml``:

.. code-block:: toml

   [tool.pytest.ini_options]
   memray_full = true

For either file, explicitly activate tracking and retain the captures:

.. code-block:: shell

   python -m pytest --memray --memray-bin-path .memray tests/

With no ``--memray-full`` flag, the Boolean ``memray_full`` setting selects the
format; its default is false (aggregated). The flag overrides a false setting,
including ``-o memray_full=false``. Repeating the flag is harmless.
To disable an ini opt-in for one run, omit the flag and use:

.. code-block:: shell

   python -m pytest --memray -o memray_full=false --memray-bin-path .memray tests/

The flag accepts no attached value: ``--memray-full=false`` (or any other value)
is a pytest usage error. Invalid Boolean ini values, such as ``memray_full = sometimes``,
are rejected before capture setup, even when tracking is inactive or
``--memray-full`` is present. There is no separate negative flag.

Tracking boundaries and persistence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``--memray-full`` and ``memray_full`` change only the capture format. Neither
activates tracking: existing activation by ``--memray`` or markers still applies.
Full mode does not require ``--memray-bin-path``, but without a persistent path
the existing temporary-directory cleanup still applies after the run.
Capture naming and ``--memray-bin-prefix`` behavior are unchanged.

The native-frame and Python allocator options above remain independent choices;
full mode does not change allocator coverage or marker tracing overrides. It also
keeps the existing whole-test tracking window. Ordinary flame graphs show a
snapshot, normally at peak memory use; full data alone does not make every
function visible there. Temporal flame graphs allow selecting a time range.
For isolation of only part of a test, place an application-level ``memray.Tracker``
around that code and run without plugin tracking, so the two Trackers do not overlap.
