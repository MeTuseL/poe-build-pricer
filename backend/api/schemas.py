from ninja import Schema
from typing import Any, Dict

class PobDecodeResponseAny(Schema):
    data: Dict[str, Any]

class PobDecodeRequest(Schema):
    pob_string: str