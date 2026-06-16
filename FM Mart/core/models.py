from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
choices=(('Cash On delivery','Cash On delivery'),
         ('Easypaisa','Easypaisa'),
         ('Jazcash','Jazcash'),
         ('Bank Transfer','Bank Transfer'))

STATUS_CHOICES=(('Pending','Pending'),
                ('On The Way','On The Way'),
                ('Delivered','Delivered'))

# Create your models here.
class User(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Email is required.')
        user=self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True) 
        extra_fields.setdefault('is_superuser',True)

        user=self.create_user(email,password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser):
    email=models.EmailField(unique=True)
    name=models.CharField()
    phone=models.CharField(blank=True,null=True)
    city=models.CharField(blank=True,null=True)
    address=models.CharField()
    profile_image=models.ImageField(blank=True,null=True,upload_to='profiles-images/')

    
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    objects=User()

    def __str__(self):
        return self.email

    def has_perm(self,obj=None):
        return self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_superuser
    


class Items(models.Model):
    item_image=models.ImageField(upload_to='items-images')
    name=models.CharField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(max_digits=100,decimal_places=2)


class Carts(models.Model): 
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
    items=models.ManyToManyField(Items,blank=True)

    def __str__(self):
        user=str(self.user)
        return  user

class Quantity(models.Model):
    cart=models.ForeignKey(Carts,on_delete=models.CASCADE,null=True)
    quantity_items=models.ForeignKey(Items,on_delete=models.CASCADE,null=True)
    actual_price=models.DecimalField(max_digits=100,decimal_places=2,default=1)
    price_for_user=models.DecimalField(max_digits=100,decimal_places=2,default=1)
    quantity=models.PositiveIntegerField(default=0)

class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.SET_DEFAULT,default=None,null=True)
    item_relation=models.ForeignKey(Items,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField()
    email=models.EmailField()
    phone=models.CharField()
    address=models.CharField()
    city=models.CharField()
    postal_code=models.PositiveIntegerField()
    item=models.CharField(default=None)
    order_placed_at=models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField(default=None)
    price=models.CharField(default=None)
    payment_received=models.BooleanField(default=0)
    payment_method=models.CharField(choices=choices)
    status=models.CharField(choices=STATUS_CHOICES,default='Pending')






    



