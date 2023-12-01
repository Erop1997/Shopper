from django.contrib import admin
from .models import *

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Product, SlugAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(SliderImage)
admin.site.register(CartItem)
admin.site.register(Guest)
admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(Review)


# Register your models here.
