# snowpark-python-devtools

# Example

## Annotate a test

```python

@pytest.mark.snowpark_vcr
def test_method():
    pass
```

## pytest options to run tests in record and replay

### Specifying tests

```bash
# run tests which are annotated with `@pytest.mark.snowpark_vcr` in record and replay
$pytest <tests> --snowpark-record-mode annotated,  this is the default mode
# disable running record and replay mode for all the tests
$pytest <tests> --snowpark-record-mode disable
# run all the tests in record and replay regardless of whether the tests are being annotated with `@pytest.mark.snowpark_vcr`
$pytest <tests> --snowpark-record-mode all
```