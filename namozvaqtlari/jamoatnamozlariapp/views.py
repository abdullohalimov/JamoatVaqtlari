from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import District, Masjid, Region


def is_admin(user):
    return user.is_authenticated and user.is_staff
# Create your views here.

@user_passes_test(is_admin)
def your_custom_view(request):
    viloyats = Region.objects.all()
    districts = District.objects.all()
    masjids = Masjid.objects.all()
    viloyat_labels = [ viloyat.name_uz for viloyat in viloyats]
    viloyat_values = []
    district_labels = [ district.name_uz for district in districts]
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
    
    return render(request, 'jamoatnamozlariapp/custom_view.html', {'district_labels': district_labels, 'district_values': district_values, 'masjid_labels': masjid_labels, 'masjid_values': masjid_values, 'viloyat_labels': viloyat_labels, 'viloyat_values': viloyat_values})
