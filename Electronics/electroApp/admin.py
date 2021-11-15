from django.contrib import admin
from electroApp.models import PhoneOTP,User,OrderPlaced,Customer,Product,Cart,Category,Vendor,Brand,Image
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm
# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserAdminCreationForm

    list_display = ('phone',  'admin',)
    list_filter = ('staff','active' ,'admin', )
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone','name', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone','name')
    ordering = ('phone','name')
    filter_horizontal = ()


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)



class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['phone','name','state','city','locality','zipcode']

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['category','title','brand','description','MRP','discount','selling_price','onSale','image','date_added','thumbnail']
    list_filter = ['category','date_added','brand']
    prepopulated_fields = {'slug':('title',)}
    search_fields = ['category','title','brand']
    ordering = ['-date_added',]

class BrandModelAdmin(admin.ModelAdmin):
        list_display = ['title','catagory']
        list_filter = ['catagory','title']
    
class VenderModelAdmin(admin.ModelAdmin):
    list_display = ['name','created_at']

class CatagoryModeladmin(admin.ModelAdmin):
    list_display = ['title','ordering']
    prepopulated_fields = {'slug':('title',)}

class CartAdmin(admin.ModelAdmin):
    list_display = ['user_cart','product','quantity']
   
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['user','get_name','product','quantity','get_amount','order_date','get_state','status']
    
    @admin.display(ordering='Customer__state', description='Address')
    def get_state(self, obj):
        return obj.customer.locality + ', ' + obj.customer.city + ', ' + obj.customer.state + ', ' + str(obj.customer.zipcode)
    
    @admin.display(description='Name')
    def get_name(self,obj):
        return obj.customer.name
    @admin.display(description='Amount')
    def get_amount(self,obj):
        return obj.this_selling_price
    
    
admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP)
admin.site.register(Customer,CustomerModelAdmin)
admin.site.register(Brand,BrandModelAdmin)
admin.site.register(Product,ProductModelAdmin)
admin.site.register(Category)
admin.site.register(Vendor,VenderModelAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(OrderPlaced,OrderPlacedAdmin)
admin.site.register(Image)

