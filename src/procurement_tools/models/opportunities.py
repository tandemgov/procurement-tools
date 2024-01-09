from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class PtypeEnum(str, Enum):
    u = "Justification (J&A)"
    p = "Pre solicitation"
    a = "Award Notice"
    r = "Sources Sought"
    s = "Special Notice"
    o = "Solicitation"
    g = "Sale of Surplus Property"
    k = "Combined Synopsis/Solicitation"
    i = "Intent to Bundle Requirements (DoD-Funded)"


class SetAsideEnum(str, Enum):
    sba = "Total Small Business Set-Aside (FAR 19.5)"
    sbp = "Partial Small Business Set-Aside (FAR 19.5)"
    _8a = "8(a) Set-Aside (FAR 19.8)"
    _8an = "8(a) Sole Source (FAR 19.8)"
    hzc = "Historically Underutilized Business (HUBZone) Set-Aside (FAR 19.13)"
    hzs = "Historically Underutilized Business (HUBZone) Sole Source (FAR 19.13)"
    sdvosbc = (
        "Service-Disabled Veteran-Owned Small Business (SDVOSB) Set-Aside (FAR 19.14)"
    )
    sdvosbs = (
        "Service-Disabled Veteran-Owned Small Business (SDVOSB) Sole Source (FAR 19.14)"
    )
    wosb = "Women-Owned Small Business (WOSB) Program Set-Aside (FAR 19.15)"
    wosbss = "Women-Owned Small Business (WOSB) Program Sole Source (FAR 19.15)"
    edwosb = "Economically Disadvantaged WOSB (EDWOSB) Program Set-Aside (FAR 19.15)"
    edwosbss = (
        "Economically Disadvantaged WOSB (EDWOSB) Program Sole Source (FAR 19.15)"
    )
    las = "Local Area Set-Aside (FAR 26.2)"
    iee = "Indian Economic Enterprise (IEE) Set-Aside (specific to Department of Interior)"
    isbee = "Indian Small Business Economic Enterprise (ISBEE) Set-Aside (specific to Department of Interior)"
    biciv = "Buy Indian Set-Aside (specific to Department of Health and Human Services, Indian Health Services)"
    vsa = "Veteran-Owned Small Business Set-Aside (specific to Department of Veterans Affairs)"
    vss = "Veteran-Owned Small Business Sole source (specific to Department of Veterans Affairs)"


class OpportunitiesRequestParams(BaseModel):
    ptype: Optional[PtypeEnum] = None
    solnum: Optional[str] = Field(description="Solicitation Number", default=None)
    noticeid: Optional[str] = Field(description="Notice ID", default=None)
    title: Optional[str] = None
    postedFrom: str
    postedTo: str
    deptname: Optional[str] = None
    subtier: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    zip_code: Optional[str] = Field(alias="zip", default=None)
    organizationCode: Optional[str] = None
    organizationName: Optional[str] = None
    typeOfSetAside: Optional[SetAsideEnum] = None
    typeOfSetAsideDescription: Optional[str] = None
    ncode: Optional[str] = None
    ccode: Optional[str] = None
    rdlfrom: Optional[str] = None
    rdlto: Optional[str] = None
    limit: int = Field(le=1000)
    offset: int = Field(default=0)
