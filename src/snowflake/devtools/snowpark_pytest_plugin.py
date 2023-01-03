import json
import gzip
import pytest
import os

from ._vendored.vcrpy import VCR
from ._constant import SnowparkRecordMode


def _process_request_recording(request):
    new_value = '00000000-0000-0000-0000-000000000000'
    for idx, (key, value) in enumerate(request.query):
        if key in ('request_guid', 'request_id', 'requestId'):
            request.uri = request.uri.replace(value, new_value)
    #dict_body = json.loads(gzip.decompress(request.body).decode('UTF-8'))
    return request


def _process_response_recording(response):
    #dict_body = json.loads(gzip.decompress(response["body"]["string"]).decode('UTF-8'))
    print(response)
    return response


def _no_op_decoration(func):
    return func


@pytest.fixture(autouse=True)
def _vcr_marker(request):
    snowpark_record_mode = request.config.getoption('--snowpark-record-mode')
    marker = request.node.get_closest_marker('snowpark_vcr')
    if snowpark_record_mode == SnowparkRecordMode.ALL or\
            (snowpark_record_mode == SnowparkRecordMode.ANNOTATED and marker):
        request.getfixturevalue('vcr_cassette')
    else:
        return


def _update_kwargs(request, kwargs):
    marker = request.node.get_closest_marker('snowpark_vcr')
    if marker:
        kwargs.update(marker.kwargs)


@pytest.fixture
def vcr_cassette_name(request):
    """Name of the VCR cassette"""
    test_class = request.cls
    if test_class:
        return "{}.{}".format(test_class.__name__, request.node.name)
    return request.node.name


def pytest_addoption(parser):
    group = parser.getgroup('snowpark-devtools')
    group.addoption(
        '--snowpark-vcr-mode',
        action='store',
        dest='snowpark_vcr_mode',
        default=None,
        choices=['once', 'new_episodes', 'none', 'all'],
        help='Set the recording mode for VCR.py.'
    )
    group.addoption(
        '--snowpark-record-mode',
        action='store',
        dest='snowpark_record_mode',
        default='disable',
        choices=['annotated', 'disable', 'all']
    )


@pytest.fixture
def vcr_cassette(request, vcr, vcr_cassette_name):
    kwargs = {}
    _update_kwargs(request, kwargs)
    with vcr.use_cassette(vcr_cassette_name, **kwargs) as cassette:
        yield cassette


@pytest.fixture(scope='module')
def vcr(request, vcr_cassette_dir):
    kwargs = dict(
        cassette_library_dir=vcr_cassette_dir,
        path_transformer=VCR.ensure_suffix(".yaml"),
        before_record_request=_process_request_recording,
        before_record_response=_process_response_recording,
    )
    _update_kwargs(request, kwargs)
    vcr = VCR(**kwargs)
    return vcr


@pytest.fixture(scope='module')
def vcr_cassette_dir(request):
    test_dir = request.node.fspath.dirname
    return os.path.join(test_dir, 'cassettes')
