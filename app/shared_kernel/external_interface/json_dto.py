from typing import ClassVar, Dict

from pydantic import BaseModel
from shared_kernel.application.dtos import FailedOutputDto
from starlette import status
from starlette.responses import JSONResponse


class FailedJsonResponse(BaseModel):
    STATUS_CODES: ClassVar[Dict[str, int]] = {
        FailedOutputDto.RESOURCE_ERROR: status.HTTP_404_NOT_FOUND,
        FailedOutputDto.RESOURCE_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
        FailedOutputDto.RESOURCE_CONFLICT_ERROR: status.HTTP_409_CONFLICT,
        FailedOutputDto.PARAMETERS_ERROR: status.HTTP_400_BAD_REQUEST,
        FailedOutputDto.UNAUTHORIZED_ERROR: status.HTTP_401_UNAUTHORIZED,
        FailedOutputDto.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    _type: str
    _message: str

    @classmethod
    def build_by_output_dto(cls, failed_output_dto: FailedOutputDto) -> JSONResponse:
        return JSONResponse(
            status_code=cls.STATUS_CODES[failed_output_dto.type],
            content={"error_type": failed_output_dto.type, "message": failed_output_dto.message},
        )
