from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.external_interface.json_dto import FailedJsonResponse
from starlette.responses import JSONResponse


def test_failed_json_response():
    output_dto = FailedOutputDto.build_resource_error("리소스 에러 입니다.")

    actual = FailedJsonResponse.build_by_output_dto(output_dto)
    expected = JSONResponse(status_code=422, content={"message": "리소스 에러 입니다."})
    assert actual.status_code == expected.status_code
    assert actual.body == expected.body
