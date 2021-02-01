from typing import ClassVar

from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from shared_kernel.application.dtos import FailedOutputDto


class FailedJsonResponse(BaseModel):
    STATUS_CODES: ClassVar = {
        FailedOutputDto.RESOURCE_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
        FailedOutputDto.PARAMETERS_ERROR: status.HTTP_400_BAD_REQUEST,
        FailedOutputDto.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    _type: str
    _message: str

    @classmethod
    def build_by_output_dto(cls, failed_output_dto: FailedOutputDto):
        return JSONResponse(
            status_code=cls.STATUS_CODES[failed_output_dto.type], content={"message": failed_output_dto.message}
        )
