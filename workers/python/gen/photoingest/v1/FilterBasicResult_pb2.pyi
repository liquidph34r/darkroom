from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Verdict(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VERDICT_UNSPECIFIED: _ClassVar[Verdict]
    VERDICT_PASS: _ClassVar[Verdict]
    VERDICT_BORDERLINE: _ClassVar[Verdict]
    VERDICT_REJECT: _ClassVar[Verdict]
VERDICT_UNSPECIFIED: Verdict
VERDICT_PASS: Verdict
VERDICT_BORDERLINE: Verdict
VERDICT_REJECT: Verdict

class FilterBasicResult(_message.Message):
    __slots__ = ("name", "directory", "verdict", "reasons", "content_hash", "width", "height", "blur_score", "dark_clip_ratio", "bright_clip_ratio", "thumbnail_path")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    VERDICT_FIELD_NUMBER: _ClassVar[int]
    REASONS_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HASH_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    BLUR_SCORE_FIELD_NUMBER: _ClassVar[int]
    DARK_CLIP_RATIO_FIELD_NUMBER: _ClassVar[int]
    BRIGHT_CLIP_RATIO_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_PATH_FIELD_NUMBER: _ClassVar[int]
    name: str
    directory: str
    verdict: Verdict
    reasons: _containers.RepeatedScalarFieldContainer[str]
    content_hash: str
    width: int
    height: int
    blur_score: float
    dark_clip_ratio: float
    bright_clip_ratio: float
    thumbnail_path: str
    def __init__(self, name: _Optional[str] = ..., directory: _Optional[str] = ..., verdict: _Optional[_Union[Verdict, str]] = ..., reasons: _Optional[_Iterable[str]] = ..., content_hash: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., blur_score: _Optional[float] = ..., dark_clip_ratio: _Optional[float] = ..., bright_clip_ratio: _Optional[float] = ..., thumbnail_path: _Optional[str] = ...) -> None: ...

class FilterBasicResultArray(_message.Message):
    __slots__ = ("filter_basic_results",)
    FILTER_BASIC_RESULTS_FIELD_NUMBER: _ClassVar[int]
    filter_basic_results: _containers.RepeatedCompositeFieldContainer[FilterBasicResult]
    def __init__(self, filter_basic_results: _Optional[_Iterable[_Union[FilterBasicResult, _Mapping]]] = ...) -> None: ...
