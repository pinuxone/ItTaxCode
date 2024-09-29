Py library => ItTaxCode
-

Author: Giuseppe Latini
Version: 0.0.2
Date: 24/08/2024

Utility to decode individual Italian tax codes, it also handles homocoded strings

Explanation:
------------

**To install in venv:**<br />
pip install --index-url https://test.pypi.org/simple/ --no-deps ittaxcode_pinuxone<br />
(for now it is only on the test.pypi index)

**To import in project:**<br />
from ittaxcode_pinuxone import ittc


methods:
--------
ittc.check(taxcode) => boolean<br>
Return True if taxcode in valid format

ittc.birthdate(taxcode) => date<br>
Return date of birth

ittc.age(taxcode) => int<br>
Return years "completed"

ittc.sex(taxcode) => string<br>
Return "M" or "F"
