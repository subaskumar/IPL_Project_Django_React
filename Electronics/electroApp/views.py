from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from electroApp.forms import TempRegisterForm,SignUpForm,UserLoginForm,CustomerForm
from electroApp.models import User,PhoneOTP,Product,Brand,Customer,Cart,OrderPlaced
import random
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Create your views here.
from django.template.loader import render_to_string
#from django.core import serializers


from geopy.geocoders import Nominatim
import json
def Autofill_address(request):
    ENDPOINT = 'https://api.postalpincode.in/pincode/'
    zipcode = request.GET['zipcode']
    response = requests.get(ENDPOINT + zipcode)
    pincode_inf = json.loads(response.text)
    necessary_inf = pincode_inf[0]['PostOffice'][0]
    state = necessary_inf['State']
    city = necessary_inf['District']    
    data = {
        'state': state,
        'city': city  
    }
    return JsonResponse(data)
########################################################## googleAPI for auto address ##########################
#geolocator = Nominatim(user_agent="geoapiExercises")
    # Zipocde input
    # Using geocode()
    #location = geolocator.geocode(zipcode)
    # Displaying address details
    #print("Zipcode:",zipcode)
    #print("Details of the Zipcode:")
    #print(location)
########################################################## googleAPI for auto address ##########################

    
def mobile_view(request, data = None):

    mobiles = Product.objects.filter(category__title__contains = 'Phone')
    
    brands = Brand.objects.filter(catagory__title__contains = 'Phone')

    if request.is_ajax() :
        brand = request.GET.getlist('brand[]')
        #mobiles = Product.objects.all().order_by('-id')
        if len(brands)>0:
            mobiles = mobiles.filter(brand__in = brand)
            if len(mobiles) == 0:
                mobiles = Product.objects.filter(category__title__contains = 'Phone')
        t=render_to_string('Ajax/Mobile.html',{'mobiles':mobiles})
        return JsonResponse({'mobiles':t})

    context = {
        'mobiles': mobiles,
        'brands': brands
    }
    return render(request, 'electroApp/Mobile.html',context)


def product_detail_view(request,id):
    phone = Product.objects.get(id = id)
    context = {
        'phone': phone
    }
    print(phone)
    return render(request, 'electroApp/Product_detail.html',context)


def home(request):
    form = TempRegisterForm()
    sale_product = Product.objects.filter(onSale = True)
    context = {
        'form': form,
        'sale_product': sale_product
    }
    return render(request, 'electroApp/home.html',context)

def VerifyOTP(request):
    message = ''
    data = {}
    if request.method == "POST":
        form = SignUpForm(request.POST)
        phone = request.session['phone']
        print(phone)
        #phone_number = request.POST.get('phone')
        #phone = str(phone_number)
        otp = request.POST.get('otp')
        old = PhoneOTP.objects.filter(phone__iexact = phone)
        print(type(otp))
        print("databse OTP type",type(old.first().otp))
        if otp == old.first().otp:
            if form.is_valid():
                form.save()
                message = 'UserRegistered'
            else:
                pass
        else:
            message = 'Wrong OTP'
            
        data = {
            'message': message,
            'registererror': form.errors
        }
        print(message)
        print(form.errors)
    return JsonResponse(data,safe=False)


def otp_generator():
    otp = random.randint(999, 9999)
    return otp

def send_otp(phone):
    if phone:  
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        print('otp_key')
        #api_key='68b4ada4-01ca-11ec-a13b-0200cd936042'
        link = f'https://2factor.in/API/V1/68b4ada4-01ca-11ec-a13b-0200cd936042/SMS/{phone}/{otp_key}/InfinityElectro'
        result = requests.get(link, verify=False)
        return otp_key
    else:
        return False

def ValidatePhoneSendOTP(request):
    message = ''
    data = {}
    if request.method == "POST":
        form = TempRegisterForm(request.POST)
        phone_number = request.POST['phone']
        phone = str(phone_number)
        request.session['phone'] = phone
        if form.is_valid():
            otp = send_otp(phone)
            print(phone, otp)
            if otp:
                otp = str(otp)
                count = 0
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    count = old.count
                    old.count = count +1
                    old.otp = otp
                    old.save()
                    print('counter is',count)
                    
                else:
                    count = count + 1
                    PhoneOTP.objects.create(phone = phone, otp = otp, count = count)

                message = 'Sucessfully'
            #else:
            #    message = "Something's not right. Please try again."
        data = {
            'errorform': form.errors,
            'message': message,
            'phone': phone
        }
        print(type(form.errors))
        print(form.errors)
    return JsonResponse(data,safe=False)

    
##########################################Extra code of Phone validatin ###############################  
#request.session['phone'] = phone
#formerror = form.errors.as_json()#print(type(formerror))#print(formerror)#print("here Error is ",form.errors)


from django.contrib.auth import login,authenticate,logout

def login_view(request):
    #print(request.body)    # b'csrfmiddlewaretoken=G7MnfQVN2PvZLPVQmYV7eInTkhWM1ipSU0mRTSz9MBXebIHGShCr8l6KYfHiZcHi&phone=9090157149&password=subas404
    message = ''
    data = {}
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request,phone=phone, password=password)
        if user:
            login(request, user)
            message = 'loginSucessfully'
            #return redirect('home')
    else:
        message = 'invalidForm'
    data = {
        'formerror' : form.errors,
        'message' : message
    }
    print(message)
    print(type(form.errors))
    print(form.errors)
    return JsonResponse(data,safe=False)


########################Log Out View ###############################
def logout_view(request):
    logout(request)
    return redirect("home")

from django.contrib.auth.decorators import login_required

@login_required
def UserProfile(request,id):
    if id == request.user.id:    
        form = CustomerForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                phone = request.user
                print(phone)
                alter_phone = request.POST.get("alter_phone")
                name = request.POST.get("name")
                state = request.POST.get("state")
                city = request.POST.get("city")
                locality = request.POST.get("locality")
                zipcode = request.POST.get("zipcode")
                reg = Customer(phone = phone, alter_phone=alter_phone,  name=name, state=state, city=city, locality=locality, zipcode=zipcode )
                reg.save()
                data = {
                    'message': 'successfully'
                }
                return JsonResponse(data,safe=False)
            
        return render(request, 'electroApp/UserProfile.html',{'form': form})
    
    
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def password_change(request):
    message = ''
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            message = 'Password changed successfully'
        return render(request, 'registration/password_change_form.html',{'form': form, 'message': message})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'registration/password_change_form.html',{'form': form, 'message':message})

@login_required  
def Cutomer_address(request):
    customer = Customer.objects.filter(phone = request.user)
    return render(request, 'electroApp/Customer_address.html',{'customer':customer})


def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user_cart = request.user)
        print(cart_items)
        if cart_items:
            total_MRP_list = [cart.product.MRP * cart.quantity for cart in cart_items]
            total_selling_price_list = [cart.product.selling_price * cart.quantity for cart in cart_items]
            print(total_MRP_list)
            print(total_selling_price_list)
            total_MRP = 0.0
            total_amount = 0.0
            delivery_charge = 0
            for mrp in total_MRP_list:
                total_MRP = total_MRP + mrp
            for sp in total_selling_price_list:
                total_amount = total_amount + sp
            
            discount = total_MRP - total_amount
            print(total_amount)
            if total_amount < 100000:
                delivery_charge = 40
                total_amount = total_amount + delivery_charge
                print(total_amount)
            
            return render(request,'electroApp/cart.html',{'cart_items': cart_items,'total_MRP': total_MRP,
                                                        'total_amount':total_amount,'delivery_charge':delivery_charge,'discount':discount})
        else:
            return render(request, 'electroApp/empty_cart.html')

from django.db.models import Q
def add_to_cart(request):
    message = ''
    if request.method == 'POST':  
        user_cart = request.user
        product_id = request.POST.get('product_id')
        print(product_id)
        product = Product.objects.get(id = product_id)
        quantity = request.POST.get('quantity')
        cart_items = Cart.objects.filter(Q(user_cart = user_cart) & Q(product = product))
        if cart_items.exists():
            message = 'already_exit'
            print(message)
        else:
            add_cart = Cart(user_cart = user_cart, product = product, quantity = quantity)
            add_cart.save()
            message = 'item_added'
            print(message)
        data = {
            'message': message,
            'product': product.title,
            'quantity': quantity
        }
    return JsonResponse(data,safe=False)
    
def remove_to_cart(request,id):
    cart_item = Cart.objects.filter(Q(user_cart = request.user) & Q(id = id))
    cart_item.delete()
    return redirect('Cart')

def update_quantity(request):
    pm_data = request.GET['PM']
    product_id = request.GET["product_id"]
    
    quantity = 1
    cart = Cart.objects.get(Q(user_cart = request.user) & Q(product = product_id))
    if pm_data == 'plus':
        print(cart.product)
        cart.quantity = cart.quantity + 1
        cart.save()
        quantity = cart.quantity
    if pm_data == 'minus':
        print(cart)
        if cart.quantity > 1:
            cart.quantity = cart.quantity - 1
            cart.save()
            quantity = cart.quantity
        else:
            cart.quantity = cart.quantity
            quantity = cart.quantity
    data = {
        'quantity': quantity,
        'cart': cart.product.title
        
    }
    return JsonResponse(data, safe = True)
@login_required
def checkOut(request):
        cart_items = Cart.objects.filter(user_cart = request.user)
        address = Customer.objects.filter(phone = request.user)
        if cart_items:
            total_MRP_list = [cart.product.MRP * cart.quantity for cart in cart_items]
            total_selling_price_list = [cart.product.selling_price * cart.quantity for cart in cart_items]
            print(total_MRP_list)
            print(total_selling_price_list)
            total_MRP = 0.0
            total_amount = 0.0
            delivery_charge = 0
            for mrp in total_MRP_list:
                total_MRP = total_MRP + mrp
            for sp in total_selling_price_list:
                total_amount = total_amount + sp
            
            discount = total_MRP - total_amount
            print(total_amount)
            if total_amount < 100000:
                delivery_charge = 40
                total_amount = total_amount + delivery_charge
                print(total_amount)
            
            return render(request,'electroApp/checkOut.html',{'address':address,'total_MRP': total_MRP,'total_amount':total_amount,
                                                              'delivery_charge':delivery_charge,'discount':discount})
            
        return redirect('Cart')
            


def paymentDone(request):
    if request.method == 'POST':
        user = request.user
        addr_id = request.POST.get('address')
        pay_method = request.POST.get('payment')
            #request.session['phone'] = phone
        address = Customer.objects.get(Q(phone = user) & Q(id=addr_id))
        cart = Cart.objects.filter(user_cart = user)
        for c in cart:
            OrderPlaced(user = user, customer = address, product = c.product, quantity = c.quantity, this_MRP = c.product.MRP * c.quantity,
                        this_discount = c.product.discount, this_selling_price = c.product.selling_price * c.quantity ).save()
            c.delete()
            
        print(cart)
        print(address.locality)
        print(pay_method)
        return redirect('orders')
    
    
def Orders(request):
    order = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'electroApp/myOrder.html', {'order': order})