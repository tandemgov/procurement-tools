# procurement-tools

[![PyPI version](https://img.shields.io/pypi/v/procurement-tools.svg)](https://pypi.org/project/procurement-tools/)

A handy collection of python utilities and tools to navigate federal contracting.

## Features

- [x] UEI validation
- [x] Get a URL for an entity from USASpending
- [x] Get recent award data for an entity from USASpending
- [x] Lookup a FAR provision by citation
- [x] Get entity information from the SAM entity
- [x] Access innovations from the Periodic Table of Acquisition Innovations

## Usage

For full documentation, head to [the docs](https://procurement-tools.readthedocs.io/en/latest/).

```py
from procurement_tools import FAR, UEI, USASpending, PeriodicTable
print(UEI.is_valid("J7M9HPTGJ1S9"))
# True

print(USASpending.get_usaspending_URL("J7M9HPTGJ1S9"))
# 'https://www.usaspending.gov/recipient/bf1220c1-2373-042a-e8e1-33d5a29639d0-P/latest'

print(FAR.get_section("17.502-2"))
# Returns a pydantic model with the title, section number, url, and text of the section

print(PeriodicTable.get_random_innovation())
# Returns a dict with an innovation from the FAI Periodic Table of Acquisition Innovations
```

Additionally, we have the beginning of a SAM API client:

```python
from procurement_tools import get_entity
res = get_entity({"ueiSAM":"XRVFU3YRA2U5"})
print(res)
# Returns a pydantic model with the latest SAM data for a given Entity
```

## CLI Usage

Out of the box, there is a simple CLI, called `fargo`. You can use it to do things like:

```sh
fargo sam entity [UEI]
# Dumps a json of an entity's information

fargo sam opportunities --title "machine"
# Dumps a json of an entity's information

fargo usaspending [UEI] --awards
# Dumps a json of an entity's 10 most recent awards (in the last 90 days)
```

Check out [the docs](https://procurement-tools.readthedocs.io/en/latest/cli.html) for all of the CLI options

## Installation

```sh
pip install procurement-tools
```

## License

Apache 2.0
