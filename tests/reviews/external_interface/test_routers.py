from unittest import mock

from auth.application.service import AuthApplicationService
from reviews.application.dtos import CreateReviewOutputDto, FindReviewOutputDto
from reviews.application.service import ReviewApplicationService
from reviews.external_interface.json_dtos import (CreateReviewJsonRequest,
                                                  UpdateReviewJsonRequest)
from shared_kernel.application.dtos import FailedOutputDto


def test_get_review(client, app):
    application_service_mock = mock.Mock(spec=ReviewApplicationService)
    application_service_mock.find_review.return_value = (
        FailedOutputDto.build_resource_not_found_error()
    )

    # valid request but no resource
    with app.container.review_application_service.override(application_service_mock):
        response = client.get("/reviews/123-123-123")
    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "",
    }

    # valid request
    application_service_mock.find_review.return_value = FindReviewOutputDto(
        review_id="review_id_uuid",
        drink_id="drink_id_uuid",
        user_id="user_id_uuid",
        rating=4,
        comment="tastes good",
        created_at=737373737.6,
        updated_at=737373737.6,
    )
    with app.container.review_application_service.override(application_service_mock):
        response = client.get("/reviews/review_id_uuid")
    assert response.status_code == 200
    assert response.json() == {
        "review_id": "review_id_uuid",
        "drink_id": "drink_id_uuid",
        "user_id": "user_id_uuid",
        "rating": 4,
        "comment": "tastes good",
        "created_at": 737373737.6,
        "updated_at": 737373737.6,
    }


def test_get_reviews(client, app):
    application_service_mock = mock.Mock(spec=ReviewApplicationService)
    application_service_mock.find_reviews.return_value = (
        FailedOutputDto.build_parameters_error()
    )

    # valid request but no resource
    with app.container.review_application_service.override(application_service_mock):
        response = client.get("/reviews")
    assert response.status_code == 400
    assert response.json() == {
        "error_type": "Parameters Error",
        "message": "",
    }

    # valid request
    application_service_mock.find_reviews.return_value = [
        FindReviewOutputDto(
            review_id="review_id_uuid",
            drink_id="drink_id_uuid",
            user_id="user_id_uuid",
            rating=4,
            comment="tastes good",
            created_at=737373737.6,
            updated_at=737373737.6,
        ),
        FindReviewOutputDto(
            review_id="review_id_uuid2",
            drink_id="drink_id_uuid2",
            user_id="user_id_uuid2",
            rating=3,
            comment="tastes good2",
            created_at=123.123,
            updated_at=123.123,
        ),
    ]
    with app.container.user_application_service.override(application_service_mock):
        response = client.get("/reviews?drinkId=drink_id_uuid&order=newest")
    assert response.status_code == 200
    assert response.json() == [
        {
            "review_id": "review_id_uuid",
            "drink_id": "drink_id_uuid",
            "user_id": "user_id_uuid",
            "rating": 4,
            "comment": "tastes good",
            "created_at": 737373737.6,
            "updated_at": 737373737.6,
        },
        {
            "review_id": "review_id_uuid2",
            "drink_id": "drink_id_uuid",
            "user_id": "user_id_uuid2",
            "rating": 3,
            "comment": "tastes good2",
            "created_at": 123.123,
            "updated_at": 123.123,
        },
    ]


def test_create_review(client, app):
    application_service_mock = mock.Mock(ReviewApplicationService)
    auth_service_mock = mock.Mock(AuthApplicationService)

    # unauthorized token
    auth_service_mock.get_token_data.return_value = (
        FailedOutputDto.build_unauthorized_error()
    )
    application_service_mock.create_review.return_value = CreateReviewOutputDto(
        drink_id="drink_id_uuid",
        user_id="user_id_uuid",
        rating=4,
        comment="review comment",
        created_at=123.123,
        updated_at=123.123,
    )
    with app.container.review_application_service.override(application_service_mock):
        with app.container.auth_application_service.override(auth_service_mock):
            response = client.post(
                "/reviews",
                headers={
                    "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
                },
                json=CreateReviewJsonRequest(
                    drink_id="drink_id_uuid",
                    rating=4,
                    comment="review comment",
                ).dict(),
            )
        assert response.status_code == 401
        assert response.json() == {
            "error_type": "Unauthorized Error",
            "message": "",
        }

    # invalid request
    application_service_mock.create_review.return_value = (
        FailedOutputDto.build_resource_conflict_error()
    )
    with app.container.review_application_service.override(application_service_mock):
        response = client.post(
            "/reviews",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
            json=CreateReviewJsonRequest(
                drink_id="drink_id_uuid",
                rating=4,
                comment="review comment",
            ).dict(),
        )
    assert response.status_code == 409
    assert response.json() == {
        "error_type": "Resource Conflict Error",
        "message": "",
    }

    # valid request
    application_service_mock.create_review.return_value = CreateReviewOutputDto(
        drink_id="drink_id_uuid",
        user_id="user_id_uuid",
        rating=4,
        comment="review comment",
        created_at=123.123,
        updated_at=123.123,
    )
    with app.container.review_application_service.override(application_service_mock):
        response = client.post(
            "/reviews",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
            json=CreateReviewJsonRequest(
                drink_id="drink_id_uuid",
                rating=4,
                comment="review comment",
            ).dict(),
        )
    assert response.status_code == 200
    assert response.json() == {
        "drink_id": "drink_id_uuid",
        "rating": 4,
        "comment": "review comment",
        "created_at": 123.123,
        "updated_at": 123.123,
    }


def test_update_review(client, app):
    application_service_mock = mock.Mock(ReviewApplicationService)
    auth_service_mock = mock.Mock(AuthApplicationService)

    # unauthorized token
    auth_service_mock.get_token_data.return_value = (
        FailedOutputDto.build_unauthorized_error()
    )
    application_service_mock.create_review.return_value = CreateReviewOutputDto(
        drink_id="drink_id_uuid",
        user_id="user_id_uuid",
        rating=4,
        comment="review comment",
        created_at=123.123,
        updated_at=123.123,
    )
    with app.container.review_application_service.override(application_service_mock):
        with app.container.auth_application_service.override(auth_service_mock):
            response = client.put(
                "/reviews",
                headers={
                    "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
                },
                json=UpdateReviewJsonRequest(
                    review_id="review_id_uuid",
                    rating=4,
                    comment="updated review comment",
                ).dict(),
            )
        assert response.status_code == 401
        assert response.json() == {
            "error_type": "Unauthorized Error",
            "message": "",
        }

    # invalid request
    application_service_mock.create_review.return_value = (
        FailedOutputDto.build_resource_not_found_error()
    )
    with app.container.review_application_service.override(application_service_mock):
        response = client.post(
            "/reviews",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
            json=CreateReviewJsonRequest(
                drink_id="drink_id_uuid",
                rating=4,
                comment="review comment",
            ).dict(),
        )
    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "",
    }

    # valid request
    application_service_mock.create_review.return_value = CreateReviewOutputDto(
        drink_id="drink_id_uuid",
        user_id="user_id_uuid",
        rating=4,
        comment="review comment",
        created_at=123.123,
        updated_at=123.123,
    )
    with app.container.review_application_service.override(application_service_mock):
        response = client.post(
            "/reviews",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
            json=CreateReviewJsonRequest(
                drink_id="drink_id_uuid",
                rating=4,
                comment="review comment",
            ).dict(),
        )
    assert response.status_code == 200
    assert response.json() == {
        "drink_id": "drink_id_uuid",
        "rating": 4,
        "comment": "review comment",
        "created_at": 123.123,
        "updated_at": 123.123,
    }
