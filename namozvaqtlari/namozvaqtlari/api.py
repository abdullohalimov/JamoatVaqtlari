import datetime
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
    bomdod_jamoat: str
    peshin_jamoat: str
    asr_jamoat: str
    shom_jamoat: str
    hufton_jamoat: str
    location: str | None
    last_update: datetime.datetime
    is_subscribed: bool = False


class UserSchema(Schema):
    pk: int
    full_name: str
    user_id: int


# class SubscriptionsSchema(Schema):
#     pk: int
#     masjid: MasjidInfo


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
def hello(request, name: str, chat_id, lang: str):
    try:
        User.objects.update_or_create(
            user_id=chat_id, defaults={"full_name": name, "lang": lang}
        )
        return {"success": "True"}
    except:
        return {"success": "False"}


@api.get("/get-regions", response=List[RegionSchema])
def get_regions(request):
    return Region.objects.filter(is_active=True)


@api.get("/get-districts", response=List[DistrictSchema])
def get_districts(request, pk):
    return District.objects.filter(region=Region.objects.get(pk=pk), is_active=True)


@api.get("/get-masjidlar", response=List[MasjidlarListSchema])
@paginate(PageNumberPagination, page_size=5)
def get_masjidlar(request, district_id):
    return Masjid.objects.filter(district=District.objects.get(pk=district_id), is_active=True)


@api.get("/masjid-info", response=MasjidInfo)
def masjid_info(request, masjid_pk, user_id):
    masjid = Masjid.objects.get(pk=masjid_pk)
    user = User.objects.get(user_id=user_id)
    is_subscribed = Subscription.objects.filter(
        masjid=masjid, user=user
    ).exists()
    setattr(masjid, "is_subscribed", is_subscribed)
    azon = [masjid.bomdod, masjid.peshin, masjid.asr, masjid.shom, masjid.hufton]
    types = [masjid.bomdod_type, masjid.peshin_type, masjid.asr_type, masjid.shom_type, masjid.hufton_type]
    values = [masjid.bomdod_jamoat, masjid.peshin_jamoat, masjid.asr_jamoat, masjid.shom_jamoat, masjid.hufton_jamoat]
    times = [0, 0, 0, 0, 0]
        
    for i in range(0, 5):
        if types[i] == 'static':
            times[i] = values[i]
        else:
            if values[i].isdigit():
                a, b = azon[i].split(":")
                a = int(a)
                b = int(b) + int(values[i])
                if b > 60:
                    a = int(a) + 1
                    b = b - 60
                times[i] = f"{'0' if int(a) < 10 else ''}{a}:{'0' if b < 10 else ''}{b}"
            else:
                times[i] = azon[i]
    
    masjid.bomdod_jamoat = times[0]
    masjid.peshin_jamoat = times[1]
    masjid.asr_jamoat = times[2]
    masjid.shom_jamoat = times[3]
    masjid.hufton_jamoat = times[4]


    return masjid



@api.get("/masjid-statistikasi")
def masjid_statistikasi(request, masjid_pk):
    masjid = Masjid.objects.get(pk=masjid_pk)
    statistic = masjid.get_leaderboard_position()

    return {
        "success": True,
        "name_uz": masjid.name_uz,
        "name_ru": masjid.name_ru,
        "name_cyrl": masjid.name_cyrl,
        "district": {
            "pk": masjid.district.pk,
            "name_uz": masjid.district.name_uz,
            "name_ru": masjid.district.name_ru,
            "name_cyrl": masjid.district.name_cyrl,
            "region": {
                "pk": masjid.district.region.pk,
                "name_uz": masjid.district.region.name_uz,
                "name_ru": masjid.district.region.name_ru,
                "name_cyrl": masjid.district.region.name_cyrl,
            },
        },
        "statistic": statistic,
        "subscription_count": Subscription.objects.filter(masjid=masjid).count(),
    }


@api.post("/masjid-subscription")
def masjid_subscription(request, user_id, masjid_id, action):
    if action == "subscribe_to":
        try:
            user = User.objects.get(user_id=user_id)
            masjid = Masjid.objects.get(pk=masjid_id)
            Subscription.objects.get_or_create(
                user=user,
                masjid=masjid,
            )
            return {
                "success": "True",
                "masjid": {
                    "pk": masjid.pk,
                    "name_uz": masjid.name_uz,
                    "name_ru": masjid.name_ru,
                    "name_cyrl": masjid.name_cyrl,
                    "district": {
                        "pk": masjid.district.pk,
                        "name_uz": masjid.district.name_uz,
                        "name_ru": masjid.district.name_ru,
                        "name_cyrl": masjid.district.name_cyrl,
                    },
                },
            }
        except:
            return {"success": "False"}
    elif action == "unsubscribe":
        try:
            user = User.objects.get(user_id=user_id)
            masjid = Masjid.objects.get(pk=masjid_id)
            Subscription.objects.filter(
                user=user,
                masjid=masjid,
            ).delete()
            return {
                "success": "True",
                "masjid": {
                    "pk": masjid.pk,
                    "name_uz": masjid.name_uz,
                    "name_ru": masjid.name_ru,
                    "name_cyrl": masjid.name_cyrl,
                    "district": {
                        "pk": masjid.district.pk,
                        "name_uz": masjid.district.name_uz,
                        "name_ru": masjid.district.name_ru,
                        "name_cyrl": masjid.district.name_cyrl,
                    },
                },
            }
        except:
            return {"success": "False"}
    return {"success": "False"}


@api.get("/user-subscriptions", response=List[MasjidInfo])
@paginate(PageNumberPagination, page_size=5)
def user_subscriptions(request, user_id):
    masjids = []
    for masjid in Masjid.objects.filter(
        pk__in=Subscription.objects.filter(user=User.objects.get(user_id=user_id)).values_list("masjid", flat=True)
    ):
        azon = [masjid.bomdod, masjid.peshin, masjid.asr, masjid.shom, masjid.hufton]
        types = [masjid.bomdod_type, masjid.peshin_type, masjid.asr_type, masjid.shom_type, masjid.hufton_type]
        values = [masjid.bomdod_jamoat, masjid.peshin_jamoat, masjid.asr_jamoat, masjid.shom_jamoat, masjid.hufton_jamoat]
        times = [0, 0, 0, 0, 0]
            
        for i in range(0, 5):
            if types[i] == 'static':
                times[i] = values[i]
            else:
                if str(values[i]).isdigit():
                    a, b = azon[i].split(":")
                    a = int(a)
                    b = int(b) + int(values[i])
                    if b > 60:
                        a = int(a) + 1
                        b = b - 60
                    times[i] = f"{'0' if int(a) < 10 else ''}{a}:{'0' if b < 10 else ''}{b}"
                else:
                    times[i] = azon[i]
            
            masjid.bomdod_jamoat = times[0]
            masjid.peshin_jamoat = times[1]
            masjid.asr_jamoat = times[2]
            masjid.shom_jamoat = times[3]
            masjid.hufton_jamoat = times[4]

        masjids.append(masjid)

    return masjids
        


@api.get("/user-subscriptions-statistic")
def user_subscriptions(request, user_id):
    masjidlar = Subscription.objects.filter(user=User.objects.get(user_id=user_id))
    results = []
    for masjid in masjidlar:
        result = {
            "masjid": {
                "pk": masjid.masjid.pk,
                "name_uz": masjid.masjid.name_uz,
                "name_ru": masjid.masjid.name_ru,
                "name_cyrl": masjid.masjid.name_cyrl,
                "district": {
                    "pk": masjid.masjid.district.pk,
                    "name_uz": masjid.masjid.district.name_uz,
                    "name_ru": masjid.masjid.district.name_ru,
                    "name_cyrl": masjid.masjid.district.name_cyrl,
                    "region": {
                        "pk": masjid.masjid.district.region.pk,
                        "name_uz": masjid.masjid.district.region.name_uz,
                        "name_ru": masjid.masjid.district.region.name_ru,
                        "name_cyrl": masjid.masjid.district.region.name_cyrl,
                    },
                },
                "statistic": masjid.masjid.get_leaderboard_position(),
                "subscription_count": masjid.masjid.subscription_set.count(),
            },
        }
        results.append(result)
    return results


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

@api.get("mintaqa-malumotlari", response=MintaqaSchema)
def mintaqa_malumotlari(request, mintaqa_id):
    return Mintaqa.objects.get(mintaqa_id=mintaqa_id)
