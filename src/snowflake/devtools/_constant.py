from enum import Enum


_SNOWFLAKE_CREDENTIAL_HEADER_FIELDS = [
    "Authorization",
]


_SNOWFLAKE_REQUEST_ID_STRINGS = [
    "request_guid",
    "request_id",
    "requestId",
]


class SnowparkRecordMode(str, Enum):
    """Pytest options to specify running tests in record and replay mode"""

    # record and replay tests annotated with "snowpark_vcr"
    ANNOTATED = "annotated"
    # record and replay all tests
    ALL = "all"
    # do not record and replay any tests
    DISABLE = "disable"


class VcrpyRecordMode(str, Enum):
    ONCE = "once"
    NEW_EPISODES = "new_episodes"
    NONE = "none"
    ALL = "all"
