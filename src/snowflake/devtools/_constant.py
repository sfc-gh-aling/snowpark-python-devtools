from enum import Enum


class SnowparkRecordMode(str, Enum):
    # record and replay tests marked with "snowpark_vcr"
    ANNOTATED = "annotated"
    # record and replay all tests
    ALL = "all"
    # do not record and replay any tessts
    DISABLE = "disable"
