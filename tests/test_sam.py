import json
from procurement_tools.models.entity import Entity
from procurement_tools.sam import get_entity, get_opportunities
from pydantic import ValidationError
import pytest
import requests


@pytest.fixture()
def sam_results():
    with open("./tests/data/sam_results.json", "r") as fp:
        data = json.load(fp)
    return data


def test_entity_model(sam_results):
    ent = Entity(**sam_results["entityData"][0])
    assert ent.registration.uei == "XRVFU3YRA2U5"


class MockSAMEntityResponse:
    def json():
        with open("./tests/data/sam_entity_results.json", "r") as fp:
            data = json.load(fp)
        return data


class MockSAMExpandedEntityResponse:
    def json():
        with open("./tests/data/sam_results_expanded.json", "r") as fp:
            data = json.load(fp)
        return data


class MockSAMFullEntityResponse:
    def json():
        with open("./tests/data/sam_results_full.json", "r") as fp:
            data = json.load(fp)
        return data


class MockSAMIntegrityEntityResponse:
    def json():
        with open("./tests/data/sam_results_integrity.json", "r") as fp:
            data = json.load(fp)
        return data


def test_get_entity(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSAMEntityResponse

    monkeypatch.setattr(requests, "get", mock_get)
    res = get_entity(dict(ueiSAM="XRVFU3YRA2U5", includeSections="entityRegistration"))
    assert res.registration.dba_name == "JAMES & ENYART"

    # Test check for invalid UEI
    with pytest.raises(ValidationError) as error:
        get_entity(dict(ueiSAM="XRVFU3YRA2U5#$"))
    assert "UEI is not valid!" in str(error.value)


def test_get_entity_expanded(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSAMExpandedEntityResponse

    monkeypatch.setattr(requests, "get", mock_get)
    res = get_entity(
        dict(ueiSAM="XRVFU3YRA2U5", includeSections="entityRegistration,coreData")
    )
    assert res.registration.dba_name == "JAMES & ENYART"
    assert res.core_data.business_types.businessTypeList[0].business_type_code == "2X"


def test_get_entity_full(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSAMFullEntityResponse

    monkeypatch.setattr(requests, "get", mock_get)
    res = get_entity(dict(ueiSAM="ZMXAHH8M8VL8"))
    assert res.registration.legal_name == "OSHKOSH DEFENSE LLC"
    assert res.core_data.business_types.businessTypeList[0].business_type_code == "2X"
    assert res.assertions.goods_and_services.naics_list[0].naics_code == "221310"
    assert (
        res.reps_and_certs.pdf_links.far_pdf
        == "https://api.sam.gov/SAM/file-download?api_key=REPLACE_WITH_API_KEY&pdfType=1&ueiSAM=ZMXAHH8M8VL8"
    )


def test_get_entity_integrity(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSAMIntegrityEntityResponse

    monkeypatch.setattr(requests, "get", mock_get)
    res = get_entity(dict(ueiSAM="SQ64PQQWATX8"))
    assert res.registration.legal_name == "MAGNUM OPUS TECHNOLOGIES, INC"
    assert res.core_data.business_types.businessTypeList[0].business_type_code == "23"
    assert res.assertions.goods_and_services.naics_list[0].naics_code == "561110"
    assert (
        res.reps_and_certs.pdf_links.far_pdf
        == "https://api.sam.gov/SAM/file-download?api_key=REPLACE_WITH_API_KEY&pdfType=1&ueiSAM=SQ64PQQWATX8"
    )
    assert res.integrity_information.responsibility_information_count == 1
    assert (
        res.integrity_information.responsibility_information_list[0].attachment
        == "https://iae-prd-fapiis-attachments.s3.amazonaws.com/68479.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231203T134518Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=AKIAY3LPYEEXT7JTNBPZ%2F20231203%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=cab0834a1afc129cb9bf632c74f166ba56203debb6c8fc4971096481e1137421"
    )


def test_get_opportunities(sam_opportunties):
    res = get_opportunities(
        dict(title="SPRUCE", postedFrom="12/14/2023", postedTo="12/14/2023", limit=1000)
    )
    assert res["opportunitiesData"][0]["noticeId"] == "b3cf1793862c42b8929616760bac4610"
