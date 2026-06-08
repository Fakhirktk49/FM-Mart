from django import forms
from core.models import CustomUser,Order
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

phone_regex=RegexValidator(regex='^03[0-9]{9}$',message='Enter a valid Number(e.g., 03001234567 or +9230001234567)')

#password_regex=RegexValidator(pattern='^?=.*[a-z](?=.*[A-Z])(?=.*\d)(?=.*[@%!%*?&])[A-Za-z\d@$!%*?&]{8,$}',message='1.Password Must Have At least one lower,upper case letter a digit and one special character and minimum 8 digits.')
class RegistrationForm(forms.ModelForm):
    password=forms.CharField(help_text='1.Upper case\n 2.Lower case\n 3.A special character\n 4.A digit ',widget=forms.PasswordInput(attrs={'placeholder':'Enter a strong password.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}))
    conf_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password again.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}))
    class Meta:
        model=CustomUser

        fields=['email']

        widgets={
                 'email':forms.EmailInput(attrs={'placeholder':'Enter your email.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                 }
        
    def clean_email(self):
        email=self.cleaned_data.get('email')
        print('running email ...........................')

        if not email:
            raise ValidationError('Please! Enter a valid Email Adress.')
        
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email has already been registered.')
        
        return  email
    
    
    
    def clean(self):
        cleaned_data=super().clean()
       
        password=cleaned_data.get('password')
        conf_password=cleaned_data.get('conf_password')
        

        if password != conf_password:  
            self.add_error('password','Both Passwords Do Not Match.')
        return cleaned_data
    

class EditForm(forms.ModelForm):
    phone=forms.CharField(validators=[phone_regex],widget=forms.TextInput(attrs={'placeholder':'Phone: (e.g., 03001234567 or +9230001234567)','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}))
    class Meta:
        model=CustomUser

        fields=['name','city','address','profile_image','phone']

        widgets={'name':forms.TextInput(attrs={'placeholder':'Name','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                 'address':forms.TextInput(attrs={'placeholder':'Enter Your address.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                 'profile_image':forms.ClearableFileInput(attrs={'placeholder':'Upload your Profile image.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                 'city':forms.TextInput(attrs={'placeholder':'Enter city name.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                 'phone':forms.TextInput(attrs={'placeholder':'Phone: (e.g., 03001234567 or +9230001234567)','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'})
                 }
        

    def clean_phone(self):
        phone=self.cleaned_data.get('phone')
        pattern='^03[0-9]{9}$'
        if not re.match(pattern,phone):
            raise ValidationError('Enter a valid Number(e.g., 03001234567 or +9230001234567)')
        return phone
    
class ProfileImage(forms.ModelForm):
    class Meta:
        model=CustomUser

        fields=['profile_image']

        widget={ 'profile_image':forms.ClearableFileInput()}

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields='__all__'

        widget={'name':forms.TextInput(attrs={'placeholder':'Name','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                'phone':forms.TextInput(attrs={'placeholder':'Phone: (e.g., 03001234567 or +9230001234567)','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                'email':forms.EmailInput(attrs={'placeholder':'Enter your email.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                'city':forms.TextInput(attrs={'placeholder':'Enter city name.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                'address':forms.TextInput(attrs={'placeholder':'Adress.','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                'postal_code':forms.NumberInput(attrs={'placeholder':'Enter your postal code','class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'}),
                'payment_method':forms.CheckboxInput(attrs={'class':'w-full p-3 rounded-xl bg-white/10 focus:bg-white/20 outline-none transition'})}

        
    