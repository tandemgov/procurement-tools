import pytest
import requests
from procurement_tools.far import FAR
from procurement_tools.models.far_clause import Clause

SECTION_TEXT = """(a) Written agreement on responsibility for management and administration—.\n(1) Assisted acquisitions .\n(i) Prior to the issuance of a solicitation, the servicing agency and the requesting agency shall both sign a written interagency agreement that establishes the general terms and conditions governing the relationship between the parties, including roles and responsibilities for acquisition planning, contract execution, and administration and management of the contract(s) or order(s). The requesting agency shall provide to the servicing agency any unique terms, conditions, and applicable agency-specific statutes, regulations, directives, and other applicable requirements for incorporation into the order or contract. In the event there are no agency unique requirements beyond the FAR, the requesting agency shall so inform the servicing agency contracting officer in writing. For acquisitions on behalf of the Department of Defense, also see subpart\xa0 17.7 . For patent rights, see 27.304-2 . In preparing interagency agreements to support assisted acquisitions, agencies should review the Office of Federal Procurement Policy (OFPP) guidance, Interagency Acquisitions, available at https://www.whitehouse.gov/wp-content/uploads/legacy_drupal_files/omb/assets/OMB/procurement/interagency_acq/iac_revised.pdf .\n(ii) Each agency’s file shall include the interagency agreement between the requesting and servicing agency, and shall include sufficient documentation to ensure an adequate audit consistent with 4.801 (b).\n(2) Direct acquisitions . The requesting agency administers the order; therefore, no written agreement with the servicing agency is required.\n(b) Business-case analysis requirements for multi-agency contracts and governmentwide acquisition contracts . In order to establish a multi-agency or governmentwide acquisition contract, a business-case analysis must be prepared by the servicing agency and approved in accordance with the OFPP business case guidance, available at https://www.whitehouse.gov/wp-content/uploads/legacy_drupal_files/omb/procurement/memo/development-review-and-approval-of-business-cases-for-certain-interagency-and-agency-specific-acquisitions-memo.pdf . The business-case analysis shall—\n(1) Consider strategies for the effective participation of small businesses during acquisition planning (see 7.103 (u));\n(2) Detail the administration of such contract, including an analysis of all direct and indirect costs to the Government of awarding and administering such contract;\n(3) Describe the impact such contract will have on the ability of the Government to leverage its purchasing power, e.g. , will it have a negative effect because it dilutes other existing contracts;\n(4) Include an analysis concluding that there is a need for establishing the multi-agency contract; and\n(5) Document roles and responsibilities in the administration of the contract."""


@pytest.fixture
def clause():
    return Clause(
        number="17.502-1",
        title="17.502-1 General.",
        body=SECTION_TEXT,
    )


def test_clause_url(clause):
    assert clause.url == "https://www.acquisition.gov/far/17.502-1"


class MockGithubResponse:
    # mock json() method always returns a specific testing dictionary
    status_code = 200
    with open("./tests/data/far_17.502-1.html", "r") as fp:
        text = fp.read()


def test_get_section(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockGithubResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    res = FAR.get_section("17.502-1")
    assert res.title == "17.502-1 General."
    assert res.body == SECTION_TEXT
