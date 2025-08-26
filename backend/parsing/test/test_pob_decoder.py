import pytest
from parsing.decoder import pob_decoder
import zlib
import base64


# Note => run with: python -m pytest parsing/test -v

def test_decode_pob_code_roundtrip():
    original_xml = "<PathOfBuilding><Items></Items></PathOfBuilding>"

    compressed = zlib.compress(original_xml.encode("utf-8"))
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8").rstrip("=")

    decoded = pob_decoder.decode_pob_code(encoded)
    assert decoded == original_xml


def test_decode_pob_code_invalid_padding():
    original_xml = "<A></A>"

    compressed = zlib.compress(original_xml.encode("utf-8"))
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8").rstrip("=")

    encoded_no_padding = encoded.rstrip("=")

    decoded = pob_decoder.decode_pob_code(encoded_no_padding)
    assert decoded == original_xml


def test_decode_pob_code_invalid_input():
    with pytest.raises(Exception):
        pob_decoder.decode_pob_code("invalid!!not_base64")