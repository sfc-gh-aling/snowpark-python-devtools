# snowpark-python-devtools

# Installation from source code

```bash
$git clone git@github.com:sfc-gh-aling/snowpark-python-devtools.git
$cd snowpark-python-devtools
$git checkout -b dev origin/dev
$pip install .
```

# Example

## Annotate a test to run with record and replay

```python

@pytest.mark.snowpark_vcr
def test_method():
    pass
```

## pytest options to run tests in record and replay

### Specifying tests

```bash
# run tests which are annotated with `@pytest.mark.snowpark_vcr` in record and replay, this is the default mode
$pytest <tests> --snowpark-record-mode annotated
# disable running record and replay mode for all the tests
$pytest <tests> --snowpark-record-mode disable
# run all the tests in record and replay regardless of whether the tests are being annotated with `@pytest.mark.snowpark_vcr`
$pytest <tests> --snowpark-record-mode all
```