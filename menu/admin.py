from django.contrib import admin
from menu.models import Category, FoodItem

#make slug field populated automatically from category name
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name','vendor__vendor_name')


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title','category','vendor','price','is_available','updated_at')
    search_fields = ('food_title','category__category_name','vendor__vendor_name','price')
    list_filter = ('is_available',)

# Register your models here.

admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem,FoodItemAdmin)
