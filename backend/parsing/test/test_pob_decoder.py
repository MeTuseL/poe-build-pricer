import base64
import zlib
import pytest
from parsing.decoder.pob_decoder import decode_pob_code

# note => terminal pytest command: python -m pytest parsing/test -v

def test_decode_pob_code():
    # Prepare a test XML
    original_xml = "<root><Items></Items></root>"

    # Encode in base64 urlsafe + zlib
    compressed = zlib.compress(original_xml.encode("utf-8"))
    pob_code = base64.urlsafe_b64encode(compressed).decode("utf-8")

    # Verify that decoding matches the original
    decoded_xml = decode_pob_code(pob_code)
    assert decoded_xml == original_xml