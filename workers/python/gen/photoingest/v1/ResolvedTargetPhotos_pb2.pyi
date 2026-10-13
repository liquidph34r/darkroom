from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResolvedTargetPhotos(_message.Message):
    __slots__ = ("photoTargets",)
    PHOTOTARGETS_FIELD_NUMBER: _ClassVar[int]
    photoTargets: _containers.RepeatedCompositeFieldContainer[PhotoTarget]
    def __init__(self, photoTargets: _Optional[_Iterable[_Union[PhotoTarget, _Mapping]]] = ...) -> None: ...

class PhotoTarget(_message.Message):
    __slots__ = ("name", "directory")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    name: str
    directory: str
    def __init__(self, name: _Optional[str] = ..., directory: _Optional[str] = ...) -> None: ...
