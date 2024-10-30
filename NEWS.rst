News
====

Lists of changes between versions.

Latest
------
* Minor: licensecheck part of release step instead of test step.

2.5.0
-----
* Minor: Add and use bouillon.git.working-directory-updated() which check that local is up to date with remote.
* Minor: news_files, build_steps, lint_steps, test_steps can be set to nothing to disable them.
* Minor: Unified cli arguments.

2.4.0
-----
* Minor: Improved cli input handling and help description.

2.3.1
-----
* Patch: Fixed case where error would not halt the release.

2.3.0
-----
* Minor: Read settings from input file (default: pyproject.toml).
* Minor: Changed default branch from master to main.
* Minor: Pypy support.

2.2.0
-----
* Minor: Added bouillon cli on install.
* Minor: Added bouillon.default_branch() which find the name of the default branch.
* Minor: Support Python 3.13.
* Minor: Use brundle to run all linters.
* Minor: Dropped setup, lint, test and upgrade commands from example boil.py.

2.1.0
-----
* Minor: Use licensecheck instead of liccheck.
* Minor: Added type marker.

2.0.0
------
* Major: Moved dependencies and project and tools configuration to pyproject.toml.
* Major: Removed docker related functionality.
* Minor: Added boil 'lint' command running isort, liccheck and ruff.
* Minor: Dropped flake8.
* Minor: Rename static kwarg to mypy in boil.py
* Minor: Support ignoring files that matches provided strings in check_for_test_files.

1.4.0
-----
* Major: Dropped Python 3.6 and 3.7 support.
* Minor: Added Python 3.11 and 3.12 support.
* Minor: Dropped pipenv dependency.
* Minor: Dropped vulnerabilities check using 'safety' in template.
* Minor: Dropped check of installed packages using 'requirementz' in template.

1.3.0
-----
* Minor: Upgraded dependencies.

1.2.0
-----
* Minor: Upgraded dependencies.

1.1.0
-----
* Minor: Upgraded dependencies.
* Minor: Full Windows support.
* Minor: Install new dependencies when upgrading.

1.0.0
-----
* Minor: Tested on Windows (excluding 'safety check').
* Minor: Added logging (use --log-level and --log-file).

0.2.0
-----
* Minor: Tested on MacOs.
* Minor: Warn instead of assert if shell==True in run.
* Patch: Fixed used of prefix in check_for_test_files.
* Patch: Fixed repository_name function.

0.1.0
-----
* Minor: Added checks during release.

0.0.5
-----
* Minor: Added security vulnerabilities check using 'safety'.
* Minor: Added docstrings check using 'flake8-docstrings'.
* Minor: Git releated functionality moved to bouillon.git.*

0.0.1
-----
* Initial release.
