import abc
from typing import ClassVar

from pydantic import BaseModel


class OutputDto(BaseModel, abc.ABC):
    status: str


class FailedOutputDto(OutputDto):
    RESOURCE_ERROR: ClassVar = "ResourceError"
    PARAMETERS_ERROR: ClassVar = "ParametersError"
    SYSTEM_ERROR: ClassVar = "SystemError"

    status: str
    message: str

    @classmethod
    def build_from_invalid_request_object(cls, message: str = ""):
        return cls(status=cls.PARAMETERS_ERROR, message=message)

    @classmethod
    def build_resource_error(cls, message: str = ""):
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message: str = ""):
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message: str = ""):
        return cls(cls.PARAMETERS_ERROR, message)
