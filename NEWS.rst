News
====

Lists of changes between versions.

1.4.0
-----
* Major: Added Python 3.11 and 3.12 support.
* Major: Dropped Python 3.6 and 3.7 support.
* Minor: Dropped pipenv dependdency.
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
