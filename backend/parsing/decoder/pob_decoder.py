import base64
import zlib

def decode_pob_code(pob_code: str) -> str:
    """
    Decode a PoB code (base64 urlsafe + zlib) into raw XML.
    """
    pob_code = pob_code.strip()
    missing_padding = len(pob_code) % 4
    if missing_padding:
        pob_code += '=' * (4 - missing_padding)
    decoded = base64.urlsafe_b64decode(pob_code)
    return zlib.decompress(decoded).decode('utf-8')