import abc
from typing import ClassVar

from pydantic import BaseModel


class SuccessOutputDto(BaseModel, abc.ABC):
    def __bool__(self) -> bool:
        return True


class FailedOutputDto(BaseModel):
    RESOURCE_ERROR: ClassVar = "ResourceError"
    PARAMETERS_ERROR: ClassVar = "ParametersError"
    SYSTEM_ERROR: ClassVar = "SystemError"

    type: str
    message: str

    @classmethod
    def build_from_invalid_request_object(cls, message: str = ""):
        return cls(type=cls.PARAMETERS_ERROR, message=message)

    @classmethod
    def build_resource_error(cls, message: str = ""):
        return cls(type=cls.RESOURCE_ERROR, message=message)

    @classmethod
    def build_system_error(cls, message: str = ""):
        return cls(type=cls.SYSTEM_ERROR, message=message)

    @classmethod
    def build_parameters_error(cls, message: str = ""):
        return cls(type=cls.PARAMETERS_ERROR, message=message)

    def __bool__(self) -> bool:
        return False
