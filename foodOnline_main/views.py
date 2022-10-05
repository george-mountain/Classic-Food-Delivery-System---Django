from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor


def home(request):
    # return HttpResponse('Hello World!')

    # let's filter out the vendors that are approved and active
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)[:8] # filter only 8 data
    context = {
        'vendors':vendors,
    }
    return render(request,'home.html',context)