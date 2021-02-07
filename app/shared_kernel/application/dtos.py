import abc
from typing import ClassVar

from pydantic import BaseModel


class SuccessOutputDto(BaseModel, abc.ABC):
    @property
    def status(self) -> bool:
        return True


class FailedOutputDto(BaseModel):
    RESOURCE_ERROR: ClassVar[str] = "ResourceError"
    PARAMETERS_ERROR: ClassVar[str] = "ParametersError"
    SYSTEM_ERROR: ClassVar[str] = "SystemError"
    UNAUTHORIZED_ERROR: ClassVar[str] = "UnauthorizedError"

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

    @classmethod
    def build_unauthorized_error(cls, message: str = ""):
        return cls(type=cls.UNAUTHORIZED_ERROR, message=message)

    @property
    def status(self) -> bool:
        return False
