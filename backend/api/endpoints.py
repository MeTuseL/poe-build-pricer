from ninja import Router
from .schemas import PobDecodeRequest, PobDecodeResponseAny
from parsing.decoder.pob_decoder import pob_xml_to_json, decode_pob_code

router = Router()

@router.post("/decode", response=PobDecodeResponseAny)
def decode_pob_endpoint(request, payload: PobDecodeRequest):
    """
    Décode un PoB string envoyé dans le body JSON et retourne un JSON structuré.
    """
    try:
        # 1️⃣ Décoder le code PoB en XML
        pob_xml = decode_pob_code(payload.pob_string)

        # 2️⃣ Convertir le XML en JSON structuré
        parsed_data = pob_xml_to_json(pob_xml)

        return {"data": parsed_data}

    except Exception as e:
        # On renvoie un message d'erreur simple
        return {"data": {"error": str(e)}}