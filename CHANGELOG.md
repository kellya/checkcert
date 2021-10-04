# Changelog

## v0.6.0 (2021-10-04)

#### New Features

* add separator for --san-only
#### Fixes

* default valid output text to "false", override with "--valid"
#### Docs

* update docs to reflect all current options
* add installation section
* enable rtd theme
* add rough intro to test rtd integration
* add docs dir for handling sphinx-based documentation
#### Others

* add docs to make

Full set of changes: [`v0.5.0...v0.6.0`](https://git.admin.franklin.edu/tins/checkcert/compare/v0.5.0...v0.6.0)

## v0.5.0 (2021-10-04)

#### New Features

* add ability to output just the sans in a space separated list
#### Refactorings

* use Any as a workaround for specific types that haven't been imported yet
* add type hints to all functions
* cleanup main logic to reduce branches

Full set of changes: [`v0.4.0...v0.5.0`](https://git.admin.franklin.edu/tins/checkcert/compare/v0.4.0...v0.5.0)

## v0.4.0 (2021-10-01)

#### New Features

* add text output for cert validity in addition to color
#### Refactorings

* align output data rather than heading for output
#### Docs

* update readme with more details
#### Others

* add ci directory for test input data
* correct lint error on file encoding
* add test for file input

Full set of changes: [`v0.3.0...v0.4.0`](https://git.admin.franklin.edu/tins/checkcert/compare/v0.3.0...v0.4.0)

## v0.3.0 (2021-10-01)

#### New Features

* add option to get host names from an external file
#### Refactorings

* clean-up for pylint
#### Docs

* update docs with a _little_ more detail
#### Others

* fix spelling
* refactor test code for pep8
* update tests to handle all branches

Full set of changes: [`v0.2.0...v0.3.0`](https://git.admin.franklin.edu/tins/checkcert/compare/v0.2.0...v0.3.0)

## v0.2.0 (2021-09-30)

#### New Features

* add color output for validity check of cert
* add option to display the text version of the x509 cert
#### Fixes

* remove duplication of output
#### Others

* add base coverage for all functions
* add initial test cases
