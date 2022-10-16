from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.models import UserProfile

from accounts.views import check_role_customer
from accounts.forms import UserForm, UserProfileForm,UserInfoForm
from django.contrib import messages

from orders.models import Order, OrderedFood
import simplejson as json



@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user) #for prepopulating form at cprofile
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form = UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile Updated Successfully!')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)


    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request,'customers/cprofile.html',context)


def my_orders(request):
    #  retrieve the orders and send to my orders page via the context
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
        'orders_count':orders.count(),
    }
    return render(request, 'customers/my_orders.html',context)



def order_detail(request,order_number):
    #  retrieve data correpsonding to the order number and push to the order detail page
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity )
        
        tax_data = json.loads(order.tax_data)

        context = {
            'order': order,
            'ordered_food':ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'customers/order_detail.html',context)
    except:
        return redirect('customer')
   