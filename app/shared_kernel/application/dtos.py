import abc
from typing import ClassVar

from pydantic import BaseModel


class SuccessOutputDto(BaseModel, abc.ABC):
    @property
    def status(self) -> bool:
        return True


class FailedOutputDto(BaseModel):
    RESOURCE_ERROR: ClassVar[str] = "Resource Error"
    RESOURCE_NOT_FOUND_ERROR: ClassVar[str] = "Resource Not Found Error"
    RESOURCE_CONFLICT_ERROR: ClassVar[str] = "Resource Conflict Error"
    PARAMETERS_ERROR: ClassVar[str] = "Parameters Error"
    SYSTEM_ERROR: ClassVar[str] = "System Error"
    UNAUTHORIZED_ERROR: ClassVar[str] = "Unauthorized Error"

    type: str
    message: str

    @classmethod
    def build_from_invalid_request_object(cls, message: str = ""):
        return cls(type=cls.PARAMETERS_ERROR, message=message)

    @classmethod
    def build_resource_error(cls, message: str = ""):
        return cls(type=cls.RESOURCE_ERROR, message=message)

    @classmethod
    def build_resource_not_found_error(cls, message: str = ""):
        return cls(type=cls.RESOURCE_NOT_FOUND_ERROR, message=message)

    @classmethod
    def build_resource_conflict_error(cls, message: str = ""):
        return cls(type=cls.RESOURCE_CONFLICT_ERROR, message=message)

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
