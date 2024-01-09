import httpx
import json
import os
import pytest
import requests


os.environ["SAM_API_KEY"] = "NotARealKey"


class MockSAMEntityResponse:
    def json():
        with open("./tests/data/sam_entity_results.json", "r") as fp:
            data = json.load(fp)
        return data


@pytest.fixture
def sam_api_results(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSAMEntityResponse

    monkeypatch.setattr(requests, "get", mock_get)


class MockUSASRecipientResponse:
    def json():
        with open("./tests/data/usaspending_recipient_profile_results.json", "r") as fp:
            data = json.load(fp)
        return data


@pytest.fixture
def usas_recipient_api_results(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockUSASRecipientResponse

    monkeypatch.setattr(httpx, "get", mock_get)


class MockUSASAwardsResponse:
    def json():
        with open("./tests/data/usaspending_awards_data.json", "r") as fp:
            data = json.load(fp)
        return data


@pytest.fixture
def usas_awards_api_results(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockUSASAwardsResponse

    monkeypatch.setattr(httpx, "post", mock_get)


class MockSBIRSolicitationResponse:
    def json():
        with open("./tests/data/sbir_solicitations.json", "r") as fp:
            data = json.load(fp)
        return data


@pytest.fixture
def sbir_solicitations_api_results(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSBIRSolicitationResponse

    monkeypatch.setattr(httpx, "get", mock_get)


class MockSBIRAwardsResponse:
    def json():
        with open("./tests/data/sbir_awards.json", "r") as fp:
            data = json.load(fp)
        return data


@pytest.fixture
def sbir_awards_api_results(respx_mock):
    with open("./tests/data/sbir_awards.json", "r") as fp:
        data = json.load(fp)
    with open("./tests/data/sbir_awards_second.json", "r") as fp:
        data_2 = json.load(fp)
    data_3 = {"ERROR": "No record found."}
    respx_mock.get("https://www.sbir.gov/api/awards.json?rows=10000&start=0").mock(
        return_value=httpx.Response(200, json=data),
    )
    respx_mock.get("https://www.sbir.gov/api/awards.json?rows=10000&start=10000").mock(
        return_value=httpx.Response(200, json=data_2),
    )
    respx_mock.get("https://www.sbir.gov/api/awards.json?rows=10000&start=20000").mock(
        return_value=httpx.Response(200, json=data_3),
    )

    # def mock_get(*args, **kwargs):
    #     return MockSBIRAwardsResponse

    # monkeypatch.setattr(httpx, "get", mock_get)


@pytest.fixture
@pytest.mark.respx(base_url="https://api.sam.gov")
def sam_opportunties(respx_mock):
    with open("./tests/data/sam_opps.json", "r") as fp:
        data = json.load(fp)
    respx_mock.get(
        "https://api.sam.gov/opportunities/v2/search?api_key=NotARealKey&title=SPRUCE&postedFrom=12%2F14%2F2023&postedTo=12%2F14%2F2023&limit=1000&offset=0"
    ).mock(
        return_value=httpx.Response(200, json=data),
    )
