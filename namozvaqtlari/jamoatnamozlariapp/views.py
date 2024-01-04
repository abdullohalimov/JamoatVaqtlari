from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import District, Masjid, Region
from django.db.models import Count


def is_admin(user):
    return user.is_authenticated and user.is_staff


# Create your views here.


@user_passes_test(is_admin)
def region_statistics(request):
    regions = Region.objects.all()

    # Calculate subscriber count for each region
    region_stats = []
    for region in regions:
        subscriber_count = Masjid.objects.filter(district__region=region).count()
        region_stats.append(
            {"name": region.name_uz, "subscriber_count": subscriber_count}
        )

    # Sort region_stats based on subscriber_count (ascending by default)
    sort_order = request.GET.get("sort", "desc")
    region_stats = sorted(
        region_stats,
        key=lambda x: x["subscriber_count"],
        reverse=(sort_order == "desc"),
    )

    context = {"region_stats": region_stats}
    return render(request, "jamoatnamozlariapp/region_statistics.html", context)


@user_passes_test(is_admin)
def district_statistics(request):
    districts = District.objects.all()

    # Calculate subscriber count for each district
    district_stats = []
    for district in districts:
        subscriber_count = Masjid.objects.filter(district=district).count()
        district_stats.append(
            {"name": district.name_uz, "subscriber_count": subscriber_count}
        )

    # Sort district_stats based on subscriber_count (ascending by default)
    sort_order = request.GET.get("sort", "desc")
    district_stats = sorted(
        district_stats,
        key=lambda x: x["subscriber_count"],
        reverse=(sort_order == "desc"),
    )

    context = {"district_stats": district_stats}
    return render(request, "jamoatnamozlariapp/district_statistics.html", context)


@user_passes_test(is_admin)
def masjid_statistics(request):
    sort_order = request.GET.get("sort", "desc")

    order_field = (
        "-subscription_count" if sort_order == "desc" else "subscription_count"
    )
    masjid_stats = Masjid.objects.annotate(
        subscription_count=Count("subscription")
    ).order_by(order_field)

    return render(
        request,
        "jamoatnamozlariapp/masjid_statistics.html",
        {"masjid_stats": masjid_stats, "sort_order": sort_order},
    )


# views.py

from django.shortcuts import render
from .models import Region, District, Masjid


@user_passes_test(is_admin)
def your_custom_view(request):
    viloyats = Region.objects.all()
    districts = District.objects.all()
    masjids = Masjid.objects.all()
    viloyat_labels = [viloyat.name_uz for viloyat in viloyats]
    viloyat_values = []
    district_labels = [district.name_uz for district in districts]
    district_values = []
    masjid_labels = [masjid.name_uz for masjid in masjids]
    masjid_values = [masjid.subscription_set.all().count() for masjid in masjids]
    for region in viloyats:
        masjids = Masjid.objects.filter(district__region=region)
        users = set()
        for masjid in masjids:
            users.add(masjid.subscription_set.all())

        viloyat_values.append(len(users))

    for district in districts:
        masjids = Masjid.objects.filter(district=district)
        users = set()
        for masjid in masjids:
            users.add(masjid.subscription_set.all())

        district_values.append(len(users))
        # Fetch data from your models and convert to a list of dictionaries

    return render(
        request,
        "jamoatnamozlariapp/custom_view.html",
        {
            "district_labels": district_labels,
            "district_values": district_values,
            "masjid_labels": masjid_labels,
            "masjid_values": masjid_values,
            "viloyat_labels": viloyat_labels,
            "viloyat_values": viloyat_values,
        },
    )
