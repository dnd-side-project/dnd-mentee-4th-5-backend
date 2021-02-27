from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from auth.application.dtos import GetTokenInputDto
from auth.external_interface.json_dto import GetTokenJsonRequest, GetTokenJsonResponse
from container import Container
from shared_kernel.external_interface.json_dto import FailedJsonResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=GetTokenJsonResponse)
@inject
def get_token(
    request: GetTokenJsonRequest, auth_application_service=Depends(Provide[Container.auth_application_service])
):
    input_dto = GetTokenInputDto(
        user_id=request.user_id,
        password=request.password,
    )
    output_dto = auth_application_service.get_token(input_dto=input_dto)
    if output_dto.status:
        return GetTokenJsonResponse(access_token=output_dto.access_token)
    return FailedJsonResponse.build_by_output_dto(output_dto)


# def verify_token():
#     def _verfiy_token(
#         request: Request,
#         auth_application_service=Depends(Provide[Container.auth_application_service]),
#         access_token: str = Header(...),
#     ):
#         input_dto = VerifyTokenInputDto(access_token=access_token, user_id=request.user_id)
#         output_dto = auth_application_service.verfiy_token(input_dto)
#         if not output_dto.result:
#             return HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         return True
#
#     return _verfiy_token
