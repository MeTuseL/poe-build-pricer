from ninja import Router
from .schemas import PobDecodeRequest, PobDecodeResponseAny, PobPriceResponseAny
from parsing.decoder.pob_decoder import pob_xml_to_json, decode_pob_code
from parsing.pricing.poeninja_pricer import add_prices_to_json

router = Router()

@router.post("/decode", response=PobDecodeResponseAny)
def decode_pob_endpoint(request, payload: PobDecodeRequest):
    """
    Décode un PoB string envoyé dans le body JSON et retourne un JSON structuré.
    """
    try:
        #  Décoder le code PoB en XML
        pob_xml = decode_pob_code(payload.pob_string)

        # Convertir le XML en JSON structuré
        parsed_data = pob_xml_to_json(pob_xml)

        return {"data": parsed_data}

    except Exception as e:
        # On renvoie un message d'erreur simple
        return {"data": {"error": str(e)}}

@router.post("/price", response=PobPriceResponseAny)
def price_pob_endpoint(request, payload: PobDecodeRequest):
    """
    Décode un PoB string dans le body JSON et retourne un JSON structuré et ajoute les prix via add_prices_to_json().
    """
    try:
        # Décoder le PoB en JSON
        pob_xml = decode_pob_code(payload.pob_string)
        parsed_data = pob_xml_to_json(pob_xml)

        # Ajouter les prix
        priced_data = add_prices_to_json(parsed_data)

        return {"data": priced_data}
    except Exception as e:
        return {"data": {"error": str(e)}}