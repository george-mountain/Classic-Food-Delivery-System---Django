from django.contrib import admin

from marketplace.models import Cart

# cart admin

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','fooditem','quantity','updated_at')

#register models 
admin.site.register(Cart,CartAdmin)

