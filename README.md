# Introduction

snowpark-python-devtools is designed to enhance local development experiences for applications
built on top of snowflake-connector-python. Libraries like snowpark-python or snowflake-sqlalchemy which depends
on the connector for http communication can also take advantage of the tool.

snowpark-python-devtools provides the following features:

1. Record and replay http based tests for faster local development


# Installation from source code

```bash
$git clone git@github.com:sfc-gh-aling/snowpark-python-devtools.git
$cd snowpark-python-devtools
$git checkout -b dev origin/dev
$pip install .
```

# Examples fore record and replay

## Annotate a test to run with record and replay

```python
# Annotate the test to run in record and replay mode
@pytest.mark.snowpark_vcr
def test_method():
    pass
```

## vcrpy configuration

### Customized vcrpy config per test case

```python
vcr_config = {
    'path': '<path_to_recording>'
    # for more configs please refer to: https://vcrpy.readthedocs.io/en/latest/configuration.html
}
@pytest.mark.snowpark_vcr(**vcr_config)
def test_method_passing_vcr_config():
    pass
```

### Global pytest fixture

snowpark-python-devtools pytest plugin will read the pytest fixture `snowpark_vcr_config` to create module-scope
VCR instance. If configs are also provided through pytest marker kwargs, then
the global fixture configs will be overridden.

```python
@pytest.fixture(scope="module")
def snowpark_vcr_config():
    return {
        # your vcr config dict
    }
```

## pytest options to run tests in record and replay

### Specifying tests

```bash
# run tests which are annotated with `@pytest.mark.snowpark_vcr` in record and replay, this is the default mode
$pytest <tests> --snowpark-record-tests-selection annotated
# disable running record and replay mode for all the tests
$pytest <tests> --snowpark-record-tests-selection disable
# run all the tests in record and replay regardless of whether the tests are being annotated with `@pytest.mark.snowpark_vcr`
$pytest <tests> --snowpark-record-tests-selection all
```
