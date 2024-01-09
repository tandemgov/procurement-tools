from .models.entity import Entity
from .models.opportunities import OpportunitiesRequestParams
from .uei import UEI
import httpx
from getpass import getpass
import keyring
from random import choice
from string import digits
import os
from pydantic import BaseModel, Field, field_validator, ValidationError
import requests
from urllib.parse import urlencode

API_KEY = os.environ.get("SAM_API_KEY")
if not API_KEY:
    try:
        API_KEY = keyring.get_password("system", "sam_api_key")
    except keyring.errors.NoKeyringError:
        API_KEY = getpass(prompt="Please enter your SAM API KEY")
BASE_URL = f"https://api.sam.gov/entity-information/v3/entities?api_key={API_KEY}"


class EntityRequestParams(BaseModel):
    """Query Parameters for a SAM API Request"""

    ueiSAM: str = None
    naicsCode: str = None
    includeSections: str = Field(default="All")

    @field_validator("ueiSAM")
    @classmethod
    def uei_is_valid(cls, uei: str) -> str:
        if UEI.is_valid(uei):
            return uei
        raise ValueError("UEI is not valid!")


def get_entity(params: dict) -> Entity:
    """Get a pydantic model of an Entity from the `SAM API <https://open.gsa.gov/api/entity-api/>`_.

    Typical usage::

        from procurement_tools import get_entity
        res = get_entity({ueiSAM:"XRVFU3YRA2U5"})

    Args:
        params: A dict for the request parameters to the SAM API. As currently implemented, we use \
        EntityRequestParams to check whether the parameters are valid. This is limited to `ueiSAM` and \
        `includeSections`

    Returns:
        A pydantic Entity modle
    """
    try:
        request_params = EntityRequestParams(**params).model_dump(exclude_none=True)
    except ValidationError:
        raise

    BASE_URL = f"https://api.sam.gov/entity-information/v3/entities?api_key={API_KEY}"

    param_str = urlencode(request_params)
    url = f"{BASE_URL}&{param_str}"
    res = requests.get(url)
    data = res.json()
    return Entity(**data["entityData"][0])


class SAM:
    def get_full_opportunities(params: dict) -> dict:
        seed = "".join(choice(digits) for i in range(13))
        mode = params.get("mode", "ALL")
        active = params.get("active", "true")
        BASE_URL = f"https://sam.gov/api/prod/sgs/v1/search/?random={seed}&index=opp&page=0&sort=-modifiedDate&size=1000&mode=search&responseType=json&qMode={mode}&is_active={active}"

        param_str = urlencode(params)
        url = f"{BASE_URL}&{param_str}"
        res = httpx.get(url)
        data = res.json()
        return data


def get_opportunities(params: dict) -> dict:
    """Get a JSON of an opportunity from the `SAM API <https://open.gsa.gov/api/get-opportunities-public-api>`_.

    Typical usage::

        from procurement_tools import get_opportunities
        res = get_opportunities({"postedFrom":"12/14/2023", "postedTo": "12/14/2023", "limit": 1000})

    Args:
        params: A dict for the request parameters to the SAM API. As currently implemented, we use \
        OpportunitiesRequestParams to check whether the parameters are valid.

    Returns:
        A dict
    """

    try:
        request_params = OpportunitiesRequestParams(**params).model_dump(
            exclude_none=True
        )
    except ValidationError:
        raise

    BASE_URL = f"https://api.sam.gov/opportunities/v2/search?api_key={API_KEY}"

    param_str = urlencode(request_params)
    url = f"{BASE_URL}&{param_str}"
    res = httpx.get(url)
    data = res.json()
    return data
