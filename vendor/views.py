
from django.shortcuts import render,get_object_or_404,redirect

from accounts.models import UserProfile
from vendor.models import Vendor
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor


@login_required
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user) # import from django.shortcuts
    vendor = get_object_or_404(Vendor,user=request.user)

    #checking to store information from the profile form entered by vendor.
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile) 
        vendor_form = VendorForm(request.POST,request.FILES,instance=vendor) 
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Restaurant Profile Update successfully!')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    
    else:
    # passing the instance profile and vendor loads the content of the existing form on our html render
        profile_form = UserProfileForm(instance=profile) # make this class on the forms.py of account and import here.
        vendor_form = VendorForm(instance=vendor)  #import this from .forms which is the forms.py of the account

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html',context)
