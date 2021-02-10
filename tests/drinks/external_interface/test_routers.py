import json
import uuid

import pytest
from drinks.domain.value_objects import DrinkType


@pytest.fixture()
def sample_drink_list():
    drink_dicts = [
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_1")),
            "drink_name": "wine_1",
            "drink_image_url": "picture_wine_1",
            "drink_type": "wine",
        },
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_2")),
            "drink_name": "wine_2",
            "drink_image_url": "picture_wine_2",
            "drink_type": "wine",
        },
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_3")),
            "drink_name": "wine_3",
            "drink_image_url": "picture_wine_3",
            "drink_type": "wine",
        },
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_4")),
            "drink_name": "beer_1",
            "drink_image_url": "picture_beer_1",
            "drink_type": "beer",
        },
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_5")),
            "drink_name": "beer_2",
            "drink_image_url": "picture_beer_2",
            "drink_type": "beer",
        },
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_6")),
            "drink_name": "beer_3",
            "drink_image_url": "picture_beer_3",
            "drink_type": "beer",
        },
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_7")),
            "drink_name": "liquor_1",
            "drink_image_url": "picture_liquor_1",
            "drink_type": "liquor",
        },
        {
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_8")),
            "drink_name": "liquor_2",
            "drink_image_url": "picture_liquor_2",
            "drink_type": "liquor",
        },
    ]
    return drink_dicts


def test_post_drinks(client):
    response = client.post(
        "/drinks",
        json={
            "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_1")),
            "drink_name": "wine_1",
            "drink_image_url": "picture_wine_1",
            "drink_type": "wine",
        },
    )
    assert response.status_code == 201


def test_get_drinks(client, sample_drink_list):
    for drink in sample_drink_list:
        print(drink["drink_id"])
        response = client.post(
            "/drinks",
            json={
                "drink_id": drink["drink_id"],
                "drink_name": drink["drink_name"],
                "drink_image_url": drink["drink_image_url"],
                "drink_type": drink["drink_type"],
            },
        )
        assert response.status_code == 201

    response = client.get("/drinks", json={"drink_type": "wine", "filter_type": "review", "order": "descending"})
    assert response.status_code == 200
    assert response.json()["drinks_json"] == json.dumps(
        [
            {
                "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_1")),
                "drink_name": "wine_1",
                "drink_image_url": "picture_wine_1",
                "drink_type": "wine",
            },
            {
                "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_2")),
                "drink_name": "wine_2",
                "drink_image_url": "picture_wine_2",
                "drink_type": "wine",
            },
            {
                "drink_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_3")),
                "drink_name": "wine_3",
                "drink_image_url": "picture_wine_3",
                "drink_type": "wine",
            },
        ]
    )
