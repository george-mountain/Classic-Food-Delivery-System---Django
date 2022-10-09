from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor

# import location based packages
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D 
from django.contrib.gis.db.models.functions import Distance


# helper function for user's location session
def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    else:
        return None

def home(request):
    # return HttpResponse('Hello World!')

    # check if lat in GET Request.
    if get_or_set_current_location(request) is not None:
        # copy the same filter from search view of marketplace and paste here and modify accordingly
        pnt = GEOSGeometry('POINT(%s %s)' %(get_or_set_current_location(request)))

        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=1000))
        ).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")

        for v in vendors:
            v.kms = round(v.distance.km,2)

    else:
        # let's filter out the vendors that are approved and active
        vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)[:8] # filter only 8 data
    context = {
        'vendors':vendors,
    }
    return render(request,'home.html',context)