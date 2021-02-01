from shared_kernel.application.dtos import FailedOutputDto


def test_failed_output_dto():
    actual = FailedOutputDto.build_from_invalid_request_object()
    expected = FailedOutputDto(status=FailedOutputDto.PARAMETERS_ERROR, message="")

    assert actual == expected
