from typing import Any, List
from ninja import NinjaAPI, Schema, Form
from ninja.pagination import PageNumberPagination, paginate
from jamoatnamozlariapp.models import District, Masjid, User, Region

api = NinjaAPI()


class RegionSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str


class DistrictSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str
    region: RegionSchema


class MasjidlarListSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str


class MasjidInfo(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str
    district: DistrictSchema
    photo: str
    bomdod: str
    peshin: str
    asr: str
    shom: str
    hufton: str


@api.post("/create-new-user")
def hello(request, name: str, chat_id):
    try:
        User.objects.update_or_create(user_id=chat_id, defaults={"full_name": name})
        return {"success": "True"}
    except:
        return {"success": "False"}


@api.get("/get-regions", response=List[RegionSchema])
def get_regions(request, lang="uz"):
    return Region.objects.all()


@api.get("/get-districts", response=List[DistrictSchema])
def get_districts(request, pk):
    return District.objects.filter(region=Region.objects.get(pk=pk))


@api.get("/get-masjidlar", response=List[MasjidlarListSchema])
@paginate(PageNumberPagination, page_size=5)
def get_masjidlar(request, district_id):
    return Masjid.objects.filter(district=District.objects.get(pk=district_id))


@api.get("/masjid-info", response=MasjidInfo)
async def masjid_info(request, masjid_pk):
    return Masjid.objects.get(pk=pk)