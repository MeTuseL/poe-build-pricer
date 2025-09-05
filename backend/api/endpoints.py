from ninja import Router
from .schemas import PobDecodeRequest, PobDecodeResponseAny, PobPriceResponseAny
from parsing.decoder.pob_decoder import pob_xml_to_json, decode_pob_code
from parsing.pricer.poeninja_pricer import add_prices_to_json

router = Router()

@router.post("/decode", response=PobDecodeResponseAny, tags=["Parsing"])
def decode_pob_endpoint(request, payload: PobDecodeRequest):
    """
    Decode a PoB string sent in the JSON body and return a structured JSON.
    General skeleton of the response is in "docs/parsing_route_response_exemple" (in root folder), with a complete exemple ("parser_exemple.json" file)
    """
    try:
        # Decode the PoB code into XML
        pob_xml = decode_pob_code(payload.pob_string)

        # Convert the XML into structured JSON
        parsed_data = pob_xml_to_json(pob_xml)

        return {"data": parsed_data}

    except Exception as e:
        # Return a simple error message
        return {"data": {"error": str(e)}}


@router.post("/price", response=PobPriceResponseAny, tags=["Parsing"])
def price_pob_endpoint(request, payload: PobDecodeRequest):
    """
    Decode a PoB string from the JSON body, convert it into structured JSON,
    and enrich it with prices using add_prices_to_json().
    General skeleton of the response is in "docs/parsing_route_response_exemple" (in root folder), with a complete exemple ("pricer_exemple.json"):

    """
    try:
        # Decode the PoB into JSON
        pob_xml = decode_pob_code(payload.pob_string)
        parsed_data = pob_xml_to_json(pob_xml)

        # Add pricing data
        priced_data = add_prices_to_json(parsed_data)

        return {"data": priced_data}

    except Exception as e:
        return {"data": {"error": str(e)}}
