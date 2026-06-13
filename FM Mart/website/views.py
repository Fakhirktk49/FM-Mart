from django.shortcuts import render
from website.forms import RegistrationForm,EditForm,ProfileImage,OrderForm
from core.models import CustomUser,Items,Carts,Quantity,Order
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from website.utils import email_sender
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required,permission_required
import json
from django.http import JsonResponse


# Create your views here.

def website(request):
    email_sender("hi","fakhirmasoodktk10@gmail.com")
    return render(request,'website/base.html')

class Home(ListView):
    model=Items
    template_name='website/home.html'
    context_object_name='items'

    def post(self,request):
       id=request.POST.get('id')
       print(id)
       item=Items.objects.get(id=id)
       cart=Carts.objects.filter(user=request.user)
       if cart:
            for cart in cart:    
                cart.items.add(item)
                quantity=Quantity.objects.filter(cart=cart,quantity_items=item)
                print('here...............................2')
                
                if not quantity:
                        print('here..................................1')
                        quantity=Quantity.objects.create(cart=cart,quantity_items=item,actual_price=item.price,price_for_user=item.price)
                        print(quantity)
                        quantity.quantity +=1
                        quantity.save()
                        cart.save()
                        messages.success(request,'Successfully item is added to cart.')
                        return redirect('cart')

                else:
                    messages.debug(request,'This item is already in cart.')
                    return redirect('cart')
                        
       else:
           return redirect('home')
            
      

def about(request):
    return render(request,'website/about.html')

def loginview(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email)
        print(password)

        if not email or not password:
            messages.error(request,'Email is required.')
            return redirect('login')
        
        else:
            try:
                user=authenticate(request,email=email,password=password)
            except:
                messages.error(request,'Invalid email or passwrod.')
                return redirect('login')
        
        if user:
            if user.is_active is not True:
                messages.error(request,'User is not Activated.')
                return redirect('login')
            
            if user is not None:
                login(request,user)
                return redirect('home')
            
            else:
                messages.error(request,'Invalid email or password.2')
                return redirect('login')
        
        else:
            messages.error(request,'Invalid email or password.')
            return redirect('login')
              
            
    return render(request,'website/login.html')

def register(request):
    try:
        if request.method == 'POST':
            form=RegistrationForm(request.POST,request.FILES)
            print(form.errors)
            if form.is_valid():
                password=form.cleaned_data['password']
                user=form.save(commit=False)
                user.set_password(password)
                user.save()
                Carts.objects.create(user=user)

                url64id=user.id
                email=user.email
                uid=urlsafe_base64_encode(force_bytes(url64id))
                token=default_token_generator.make_token(user)
                url=reverse('activate_account',kwargs={'uid':uid,'token':token})
                redirect_url=f'{settings.SITE_URL}{url}'
                email_sender(redirect_url,email)
                messages.success(request,'Activation link has been sent to your email click on it to activate your account.')
        else:  
            form=RegistrationForm()
    except:
        messages.error(request,'Some exception occured.Try again.')
        return redirect('register')
    return render(request,'website/register.html',{'form':form})

def activate_account(request,uid,token):
    try:
        id=force_str(urlsafe_base64_decode(uid))
        user=CustomUser.objects.filter(id=id).first()
        if not user:
            messages.error(request,'Invalid link.')
            return redirect('login')
        else:
            if default_token_generator.check_token(user,token):
                if user.is_active is True:
                    messages.debug(request,'This user has already been activated.')
                    return redirect('login')
                else:
                    user.is_active=True
                    user.save()
                    messages.success(request,'Your account has been successfully activated.')
                    return redirect('login')
                
            else:
                messages.error(request,'Invalid link or it has been expired.')
                return redirect('login')


    except:
        messages.error('Invalid link or it has been expired.')
        return redirect('login')


@login_required
def cart(request):
    cart=Carts.objects.filter(user=request.user)
    user=request.user
    orders=user.order_set.all()
    print(orders)
    for cart in cart:
        quantities=Quantity.objects.filter(cart=cart)
        print(quantities)
        
        if request.method == 'POST':
            data=json.loads(request.body)
            action=data.get("action")
            if action == 'decrease':
                id=data.get("item_id")
                quantity=Quantity.objects.get(id=id)
                if quantity.quantity > 1:
                    quantity.quantity += -1
                    quantity.save()
                    quantity.price_for_user=quantity.actual_price * quantity.quantity
                    quantity.save()
                    
                    return JsonResponse({'quantity':quantity.quantity,'price_for_user':quantity.price_for_user})
                else:
                    return redirect('cart') 
        
            if action == 'increase':
                id=data.get("item_id")
                quantity=Quantity.objects.get(id=id)
                if quantity.quantity >= 0:
                    quantity.quantity += 1
                    quantity.save()
                    quantity.price_for_user=quantity.actual_price * quantity.quantity
                    quantity.save()
                    return JsonResponse({'quantity':quantity.quantity,'price_for_user':quantity.price_for_user})
                else:
                    return redirect('cart')


    return render(request,'website/cart.html',{'quantities':quantities,'orders':orders})


def forgot_pass(request):
    return render(request,'website/forgot_pass.html')

def verify_email(request):
    return render(request,'website/verify_email.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form=ProfileImage(request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    if User.is_authenticated:
        user=request.user
    return render(request,'website/profile.html',{'user':user})

@login_required
def buy(request,id):
    if request.method == 'POST':
        try:
            if Carts.objects.filter(user=request.user):
                cart=Carts.objects.filter(user=request.user)
                for cart in cart:
                    if Quantity.objects.filter(cart=cart,id=id).first():
                        item=Quantity.objects.get(id=id)
                        quantity_of_order=item.quantity_items 
                        price_of_order=item.price_for_user
                        item_name=item.quantity_items.name
                        item_id=item.quantity_items.id
                        print(item_id)
                        item_for_relation=Items.objects.get(id=item_id)

            else:
                item=Items.objects.filter(id=id).first()
                quantity_of_order=1
                price_of_order=item.price
                item_name=item.name
                item_id=item.id
                item_for_relation=Items.objects.filter(id=item_id)

        except:
            messages.error(request,'Some exception occured.')
            return redirect('cart')

        form=OrderForm(request.POST)
        if form.is_valid():
            payment_method=form.cleaned_data['payment_method']
            form=form.save(commit=False)    
        
            form.payment_method=payment_method
            form.user=request.user
            form.item_relation=item_for_relation
        
            form.save()
            quantity=Quantity.objects.filter(id=id).first()
            quantity.delete()
            messages.success(request,'Order placed successfully.')
            return redirect('home')
        
        else:
            print(form.errors)
    else:
        form=OrderForm()
        try:     
            quantity=Quantity.objects.get(id=id)
            quantity_of_order=quantity.quantity
            price_of_order=quantity.price_for_user
            item_name=quantity.quantity_items.name
        except:
            messages.error(request,'Some exception occured.')
            return redirect('cart')
    return render(request,'website/buy.html',{'form':form,'item_name':item_name,'quantity_of_order':quantity_of_order,'price_of_order':price_of_order})

def change_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Password changed successfully.')
            return redirect('home')
    else:   
       form=PasswordChangeForm(request.user)
    return render(request,'website/change_password.html',{'form':form})

def edit_profile(request):
    id=request.user.id
    obj=CustomUser.objects.get(id=id)
    if request.method ==  'POST':
        form=EditForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            image=request.FILES.get('profile_image')
            phone=request.POST.get('phone')
            form.profile_image=image
            form.phone=phone
            form.save()
            messages.success(request,'Information successfully updated.')
            return redirect('profile')
    else:
        form=EditForm(instance=obj)
    return render(request,'website/edit_profile.html',{'form':form})

def delete_account(request):
    if request.method == 'POST':
        user=request.user
        CustomUser.objects.filter(id=request.user.id).delete()
        messages.error(request,'Your account has beeen deleted.')
        return redirect('home')
    else:
        user=request.user
    return render(request,'website/confirm_delete.html',{'profile':user})


def checkout(request,id):
    try:
        item=Items.objects.filter(id=id).first()
    except:
        messages.error(request,'Some exception occured')
        return redirect('cart')
    return render(request,'website/checkout.html',{'item':item})

def remove_from_cart(request):
    if request.method == 'POST':
        try:
            print("here........")
            id=request.POST.get('id')
            item=Items.objects.filter(id=id).first()
            cart=Carts.objects.filter(user=request.user).first()
            item_to_be_deleted=Quantity.objects.filter(cart=cart,quantity_items=item)
            print("here2.................")
            item_to_be_deleted.delete()
            messages.success(request,'Item removed from cart')
            return redirect('cart')

        except:
            messages.error(request,'Some exception occured.')
            return redirect('cart')

def view_order(request,id):
    try:
        order=Order.objects.filter(user=request.user,id=id).first()
        print(order)
        item_image=order.item_relation.item_image
        print(item_image)
        description=order.item_relation.description
        print(description)
    except:
        messages.error(request,'Some exception occured.')
        return redirect('cart')
    return render(request,'website/view_order.html',{'order':order,'item_image':item_image,'description':description})


def test_view(request):
    a=1/0
    return a