import uuid
import pytest
import os

from ._vendored.vcrpy import VCR
from ._constant import (
    SnowparkRecordMode,
    VcrpyRecordMode,
    _SNOWFLAKE_REQUEST_ID_STRINGS,
    _SNOWFLAKE_CREDENTIAL_HEADER_FIELDS,
)


def _process_request_recording(request):
    """Process request before recording

    Filter and scrub Snowflake credentials.
    """
    # filter request id
    for key, value in request.query:
        if key in _SNOWFLAKE_REQUEST_ID_STRINGS:
            request.uri = request.uri.replace(value, str(uuid.UUID(int=0)))

    # scrub account information
    # TODO: P0 fact check if there's other domains
    if request.host.endswith(".snowflakecomputing.com"):
        account = request.host.split(".snowflakecomputing.com")[0]
        # TODO: P2 allow customization on how to scrub fields,
        #  e.g., allow specifying the replaced value
        request.uri = request.uri.replace(account, "scrubbed_account")

    # TODO: P0 fact check that body does not contain Snowflake credentials
    # The following line is to note how to decompress body in request
    # dict_body = json.loads(gzip.decompress(request.body).decode('UTF-8'))

    return request


def _process_response_recording(response):
    """Process response recording"""

    # The following line is to note how to decompress body in request
    # dict_body =\
    #  json.loads(gzip.decompress(response["body"]["string"]).decode('UTF-8'))

    return response


@pytest.fixture(autouse=True)
def _snowpark_vcr_marker(request):
    snowpark_record_mode = request.config.getoption("--snowpark-record-tests-selection")
    marker = request.node.get_closest_marker("snowpark_vcr")
    if snowpark_record_mode == SnowparkRecordMode.ALL or (
        snowpark_record_mode == SnowparkRecordMode.ANNOTATED and marker
    ):
        request.getfixturevalue("vcr_cassette")
    else:
        return


def _update_kwargs(request, kwargs):
    marker = request.node.get_closest_marker("snowpark_vcr")
    if marker:
        kwargs.update(marker.kwargs)


@pytest.fixture
def snowpark_vcr_cassette_name(request):
    """Name of the VCR cassette"""
    test_class = request.cls
    if test_class:
        return "{}.{}".format(test_class.__name__, request.node.name)
    return request.node.name


def pytest_addoption(parser):
    group = parser.getgroup("snowpark-python-devtools")
    group.addoption(
        "--snowpark-vcr-mode",
        action="store",
        dest="snowpark_vcr_mode",
        default=None,
        choices=[e.value for e in VcrpyRecordMode],
        help="Set the recording mode for VCR.py. For more details, "
        "please refer to"
        " https://vcrpy.readthedocs.io/en/latest/usage.html#record-modes.",
    )
    group.addoption(
        "--snowpark-record-tests-selection",
        action="store",
        dest="snowpark_record_tests-selection",
        default=SnowparkRecordMode.ANNOTATED,
        choices=[e.value for e in SnowparkRecordMode],
        help="Select the tests to be recorded. `annotated` to "
        "record and replay annotated tests,"
        " `disable` to disable record and play, "
        "`all` to record and replay all the tests.",
    )


@pytest.fixture
def vcr_cassette(request, snowpark_vcr, snowpark_vcr_cassette_name):
    kwargs = {}
    _update_kwargs(request, kwargs)
    with snowpark_vcr.use_cassette(snowpark_vcr_cassette_name, **kwargs) as cassette:
        yield cassette


@pytest.fixture(scope="module")
def snowpark_vcr(request, snowpark_vcr_cassette_dir, snowpark_vcr_config):
    kwargs = dict(
        cassette_library_dir=snowpark_vcr_cassette_dir,
        path_transformer=VCR.ensure_suffix(".yaml"),
        before_record_request=_process_request_recording,
        before_record_response=_process_response_recording,
        filter_headers=_SNOWFLAKE_CREDENTIAL_HEADER_FIELDS,
        **(snowpark_vcr_config or {})
    )
    _update_kwargs(request, kwargs)
    vcr = VCR(**kwargs)
    return vcr


@pytest.fixture(scope="module")
def snowpark_vcr_cassette_dir(request):
    test_dir = request.node.fspath.dirname
    return os.path.join(test_dir, "cassettes")


@pytest.fixture(scope="module")
def snowpark_vcr_config():
    """
    This is the default empty config.
    Users' definition of vcrpy_config fixture will override the empty config.
    """
    return {}
