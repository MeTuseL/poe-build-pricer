from ninja import NinjaAPI
from api.endpoints import router as pob_router

api = NinjaAPI()

api.add_router("/pob/", pob_router)