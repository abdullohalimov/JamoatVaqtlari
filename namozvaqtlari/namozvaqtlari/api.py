from typing import Any, List
from ninja import NinjaAPI, Schema, Form
from ninja.pagination import PageNumberPagination, paginate
from jamoatnamozlariapp.models import (
    District,
    Masjid,
    Mintaqa,
    NamozVaqti,
    User,
    Region,
    Subscription,
)

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
    photo: str | None
    photo_file: str | None
    bomdod: str
    peshin: str
    asr: str
    shom: str
    hufton: str
    location: str | None


class UserSchema(Schema):
    pk: int
    full_name: str
    user_id: int


class SubscriptionsSchema(Schema):
    pk: int
    masjid: MasjidInfo


class MintaqaSchema(Schema):
    pk: int
    name_uz: str
    name_ru: str
    name_cyrl: str
    mintaqa_id: str
    viloyat: str


class NamozVaqtiSchema(Schema):
    pk: int
    mintaqa: MintaqaSchema
    milodiy_oy: int
    milodiy_kun: int
    xijriy_oy: int
    xijriy_kun: int
    vaqtlari: str


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
def masjid_info(request, masjid_pk):
    return Masjid.objects.get(pk=masjid_pk)


@api.post("/masjid-subscription")
def masjid_subscription(request, user_id, masjid_id, action):
    if action == "subscribe":
        try:
            Subscription.objects.get_or_create(
                user=User.objects.get(user_id=user_id),
                masjid=Masjid.objects.get(pk=masjid_id),
            )
            return {"success": "True"}
        except:
            return {"success": "False"}
    elif action == "unsubscribe":
        try:
            Subscription.objects.filter(
                user=User.objects.get(user_id=user_id),
                masjid=Masjid.objects.get(pk=masjid_id),
            ).delete()
            return {"success": "True"}
        except:
            return {"success": "False"}
    return {"success": "False"}


@api.get("/user-subscriptions", response=List[SubscriptionsSchema])
def user_subscriptions(request, user_id):
    return Subscription.objects.filter(user=User.objects.get(user_id=user_id))


@api.get("/bugungi-namoz-vaqti", response=NamozVaqtiSchema)
def bugungi_namoz_vaqti(request, mintaqa, milodiy_oy, milodiy_kun):
    return NamozVaqti.objects.get(
        mintaqa=Mintaqa.objects.get(mintaqa_id=mintaqa),
        milodiy_oy=milodiy_oy,
        milodiy_kun=milodiy_kun,
    )


@api.get("/namoz-vaqtlari", response=List[NamozVaqtiSchema])
@paginate(PageNumberPagination, page_size=5)
def namoz_vaqtlari(request, mintaqa, oy):
    return NamozVaqti.objects.filter(
        mintaqa=Mintaqa.objects.get(mintaqa_id=mintaqa), milodiy_oy=oy
    )


@api.get("/viloyat-mintaqalari", response=List[MintaqaSchema])
def viloyat_mintaqalari(request, viloyat_id):
    return Mintaqa.objects.filter(viloyat=viloyat_id)