from django.shortcuts import render,get_object_or_404
from marketplace.context_processors import get_cart_amounts, get_cart_counter
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from django.http.response import HttpResponse, JsonResponse
from marketplace.models import Cart
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_count = vendors.count()  # count the returned vendor data.
    context = {
        'vendors':vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html',context)


def vendor_detail(request,vendor_slug):
    #get the vendor and send to the html page
    vendor =  get_object_or_404(Vendor, vendor_slug=vendor_slug)
    
    #fetch all the categories that belong to the vendor
    #prefetch related to make us have access to the food items from category.
    # But to make the prefetch work, we need to set the related name to our food item model
    # set this name (fooditems) in the models.py of the menu
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )

    #accessing the cart items so that we can pass it to vendor details.html
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html',context)


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the user has already added that food item to the cart.
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    #import JsonResponse from django.http.response
                    return JsonResponse({'status':'Success','message':'Increased cart quantity','cart_counter': get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the food to the cart!','cart_counter': get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                    
            except:
                return JsonResponse({'status':'Failed','message':'This food item does not exist!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})
        

    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the user has already added that food item to the cart.
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # Decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    #import JsonResponse from django.http.response
                    return JsonResponse({'status':'Success','cart_counter': get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'Failed','message':'You do not have this item in your cart!'})
                    
            except:
                return JsonResponse({'status':'Failed','message':'This food item does not exist!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})
        

    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context ={
        'cart_items': cart_items,
    }
    return render(request,'marketplace/cart.html',context)


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # cehck if the cart item exists
            try:

                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart item deleted!','cart_counter': get_cart_counter(request),'cart_amount':get_cart_amounts(request)})
            
            except:
                return JsonResponse({'status':'Failed','message':'Cart Item does not exist!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})
    

    
