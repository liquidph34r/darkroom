from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IngestResult(_message.Message):
    __slots__ = ("completed",)
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    completed: bool
    def __init__(self, completed: _Optional[bool] = ...) -> None: ...
