from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from decimal import *

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')

        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(phone=phone)

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(phone, password=password,is_staff=True,)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone, password=password,is_staff=True,is_admin=True,)
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name        = models.CharField(max_length = 20, blank = True, null = True)
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.phone)

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex = r'^\+?1?\d{9,14}$', message="Phone Number must be contain country code ")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    count = models.IntegerField(default=0, help_text= 'Number of OTP sent')
    logged = models.BooleanField(default=False, help_text='If OTP Verification got successful')
    forgot = models.BooleanField(default=False, help_text='Only true for Forgot password')
    forgot_logged = models.BooleanField(default=False, help_text='Only true if validate OTP forgot get successful')

    def __str__(self):
        return str(self.phone) + 'is sent' + str(self.otp)

from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")    
    phone = models.ForeignKey(User, on_delete=models.CASCADE)
    alter_phone = models.CharField(validators=[phone_regex], max_length=17,null = True)
    name  = models.CharField(max_length =100, blank = False, null = False,)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    zipcode = models.IntegerField(default=0)

    def __str__(self):
        return str(self.phone)

    #@receiver(post_save, sender=User)
    #def update_customer_signal(sender, instance, created, **kwargs):
    #    if created:
    #        Customer.objects.create(phone=instance)
    #   instance.customer.save()
    

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return str(self.name)

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']
    
    def __str__(self):
        return str(self.title)

# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    catagory = models.ForeignKey(Category, related_name='CatagoryBrands', on_delete=models.CASCADE)
    image=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural='Brands'

    def __str__(self):
        return str(self.title)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='vender', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    MRP = models.FloatField()
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    selling_price = models.FloatField(default=0)
    onSale = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Products/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='Products/', blank=True, null=True)

    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.selling_price = Decimal(self.MRP) - (Decimal(self.MRP) * self.discount) /100
        super(Product, self).save(*args, **kwargs)
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

class Image(models.Model):
    item = models.ForeignKey(Product,related_name='item', on_delete=models.CASCADE, null=True, blank = True)
    images = models.ImageField(upload_to='All_Image/Products/', blank=True, null=True)
    
    def __str__(self):
        return str(self.item)
    
class Cart(models.Model):
    user_cart = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    #products    = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return str(self.id)
    
    #def get_total_item_price(self):
    #    return self.quantity * self.item.price

    #def get_discount_item_price(self):
    #    return self.quantity * self.item.discount_price

    #def get_amount_saved(self):
    #    return self.get_total_item_price() - self.get_discount_item_price()

    #def get_final_price(self):
    #    if self.item.discount_price:
    #        return self.get_discount_item_price()
    #    return self.get_total_item_price()


STATUS_CHOICES = (  ('Pending','Pending'),
                    ('Accepted','Accepted'),
                    ('Packed','Packed'),
                    ('On The Way', 'On The Way'),
                    ('Delivered','Delivered'),
                    ('Canceled','Canceled'),
                )
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default=STATUS_CHOICES[0][0])
    this_MRP = models.FloatField()
    this_discount = models.DecimalField(decimal_places=2, max_digits=10)
    this_selling_price = models.FloatField(default=0)
    
    def __str__(self):
        return self.product.title + ' for User ' + self.user.phone
    
    #def get_total_price(self):
    #    total = 0
    #    for order_item in self.items.all():
    #        total += order_item.get_final_price()
    #    return total
