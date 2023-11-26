from ninja import NinjaAPI
from jamoatnamozlariapp.models import User, Region

api = NinjaAPI()

@api.post("/create-new-user")
def hello(request, name: str, chat_id, ):
    try:
        User.objects.update_or_create(user_id=chat_id, defaults={"full_name": name})
        return {"success": "True"}
    except:
        return {"success": "False"}
    
@api.get("/get-regions")
def get_regions(request, lang = "uz"):
    regions = Region.objects.all()
    result = {}
    for region in regions:
        result[region.pk] = region.name_ru if lang == "ru" else region.name_cyrl if lang == "de" else region.name_uz
    return result