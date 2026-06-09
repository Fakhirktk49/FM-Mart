from django.contrib import admin
from .models import CustomUser,Items,Carts,Quantity,Order
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display=['name','email','phone']

    fieldsets=[('info',{'fields':['name','email','phone','address','profile_image']}),('credentials',{'fields':['is_active','is_staff','is_superuser']})]

    add_fieldsets=(
        (None,{'classes':'wide','fields':['email','password1','password2']}),
        )

   #must use baseuseradmin

    list_display=['email']
    ordering=['name']
    filter_horizontal=[]
    search_fields=['name','email']
    list_filter=['phone']


admin.site.register(CustomUser,CustomUserAdmin)

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display=['id','name','price']
    list_filter=['name']

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display=['user']
    list_filter=['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['name','order_placed_at','order_delivered']
    list_filter=['order_delivered']

admin.site.register(Quantity)