from shared_kernel.application.dtos import FailedOutputDto, SuccessOutputDto


def test_success_output_dto():
    class DerivedSuccessOutputDto(SuccessOutputDto):
        pass

    actual = DerivedSuccessOutputDto()
    if actual:
        assert True
    else:
        assert False


def test_failed_output_dto():
    actual = FailedOutputDto.build_from_invalid_request_object()
    expected = FailedOutputDto(type=FailedOutputDto.PARAMETERS_ERROR, message="")

    if not actual:
        assert True
    else:
        assert False
    assert actual == expected
