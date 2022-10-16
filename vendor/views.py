
from django.db import IntegrityError
from unicodedata import category
from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse, JsonResponse
from accounts.models import UserProfile
from menu.forms import CategoryForm, FoodItemForm
from orders.models import Order, OrderedFood
import vendor
from vendor.models import OpeningHour, Vendor
from .forms import VendorForm, OpeningHourForm
from accounts.forms import UserProfileForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

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

@login_required
@user_passes_test(check_role_vendor)
def menu_builder(request):
    # call the get_vendor helper function
    vendor = get_vendor(request) #help us to get the logged in vendor
    #use the logged in vendor to get the categories.
    #use filter instead of get to retrieve multiple results.
    categories = Category.objects.filter(vendor=vendor).order_by('created_at') #import category from menu.models

    #send the cateogries to the html page using context
    context = {
        'categories':categories,
    }
    return render(request, 'vendor/menu_builder.html',context)
@login_required
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    #call the get vendor helper function
    vendor = get_vendor(request) #help us to get the logged in vendor
    category = get_object_or_404(Category,pk=pk) #retrieve the category with the pk value

    # Filter all the food items of the category as shown below.
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    
    #pass the food item and category to the html page via context
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request,'vendor/fooditems_by_category.html',context)

@login_required
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # handle the vendor and the slug which the user is not providing but needed in DB programatically
            category_name = form.cleaned_data['category_name']  #get category name from user input
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            category.save() # The category ID will be generated here

            #append the category id to the category slug as shown below.
            category.slug = slugify(category_name)+'-'+str(category.id) #import slugify from django.template.defaultfilters 
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm() # import from menu.forms
    context = {
        'form': form,
    }
    return render(request,'vendor/add_category.html',context)

@login_required
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    #get the category instance and pass it in the form.
    category = get_object_or_404(Category, pk=pk) # this is the pk from edit url of the menu builder html
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            # handle the vendor and the slug which the user is not providing but needed in DB programatically
            category_name = form.cleaned_data['category_name']  #get category name from user input
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name) #import slugify from django.template.defaultfilters 
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category) # import from menu.forms
    context = {
        'form': form,
        'category': category,
    }
    return render(request,'vendor/edit_category.html',context)

@login_required
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk) #pk received from the delete url in menu builder html
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('menu_builder')

@login_required
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            # handle the vendor and the slug which the user is not providing but needed in DB programatically
            foodtitle = form.cleaned_data['food_title']  #get category name from user input
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            
            food.save()
            food.slug = slugify(foodtitle)+'-'+str(food.id) #import slugify from django.template.defaultfilters 
            food.save()
            messages.success(request, 'Food Item Added successfully!')
            return redirect('fooditems_by_category',food.category.id) #nb: food by category accepts pk
        else:
            print(form.errors)
    else:
        form =FoodItemForm()
        # modify this form qury set
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    # send the form content to the html using the context
    context = {
        'form': form,
    }

    return render(request,'vendor/add_food.html',context)


@login_required
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    #get the category instance and pass it in the form.
    food = get_object_or_404(FoodItem, pk=pk) # this is the pk from edit url of the menu builder html
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            # handle the vendor and the slug which the user is not providing but needed in DB programatically
            foodtitle = form.cleaned_data['food_title']  #get food name from user input
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle) #import slugify from django.template.defaultfilters 
            form.save()
            messages.success(request, 'Food Item updated successfully!')
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food) # import from menu.forms
        # modify this form qury set
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'food': food,
    }
    return render(request,'vendor/edit_food.html',context)


@login_required
@user_passes_test(check_role_vendor)
def delete_food(request,pk=None):
    food = get_object_or_404(FoodItem, pk=pk) #pk received from the delete url in menu builder html
    food.delete()
    messages.success(request, 'Food Item has been deleted successfully!')
    return redirect('fooditems_by_category',food.category.id)


def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form':form,
        'opening_hours':opening_hours,
    }
    return render(request,'vendor/opening_hours.html',context)


def add_opening_hours(request):
    # handle the AJAX data and save in the database
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            
            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request),day=day,
                from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)

                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status':'success','id':hour.id,
                        'day':day.get_day_display(),'is_closed':'Closed'}
                    else:
                        response = {'status':'success','id':hour.id,
                        'day':day.get_day_display(),'from_hour':hour.from_hour,'to_hour':hour.to_hour}

                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status':'failed','message': from_hour+'-'+to_hour+' already exists for this day!'}
                return JsonResponse(response)
        else:
            HttpResponse('Invalid Request!')


def remove_opening_hours(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success','id':pk})



def order_detail(request,order_number):

    #  retrieve order and ordered food objects and pass to the html page
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))

        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': order.get_total_by_vendor()['subtotal'],
            'tax_data': order.get_total_by_vendor()['tax_dict'],
            'grand_total': order.get_total_by_vendor()['grand_total'],
        }
    except:
        return redirect('vendor')
    return render(request,'vendor/order_detail.html',context)



def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
        
    }
    return render(request, 'vendor/my_orders.html', context)



