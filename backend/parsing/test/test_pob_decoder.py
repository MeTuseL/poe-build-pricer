import pytest
from parsing.decoder import pob_decoder
import zlib
import base64

# Note => run with: python -m pytest parsing/test -v

def test_decode_pob_code_roundtrip():
    # Prepare a minimal XML string as an example PoB export
    original_xml = "<PathOfBuilding><Items></Items></PathOfBuilding>"

    # Simulate the PoB encoding process:
    # Compress the XML with zlib
    compressed = zlib.compress(original_xml.encode("utf-8"))
    # Encode in URL-safe Base64 and strip "=" padding (PoB convention)
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8").rstrip("=")

    # Decode using our pob_decoder
    decoded = pob_decoder.decode_pob_code(encoded)

    # Ensure that after encoding + decoding we get back the original XML
    assert decoded == original_xml


def test_decode_pob_code_invalid_padding():
    # Prepare a different minimal XML string
    original_xml = "<A></A>"

    # Compress and Base64-encode as before
    compressed = zlib.compress(original_xml.encode("utf-8"))
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8").rstrip("=")

    # Simulate a broken code with missing padding by stripping "=" characters
    encoded_no_padding = encoded.rstrip("=")

    # Our decoder should still be able to handle it and return the correct XML
    decoded = pob_decoder.decode_pob_code(encoded_no_padding)

    # Verify that decoding is still successful despite the missing padding
    assert decoded == original_xml