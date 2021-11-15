from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from electroApp.models import User,Customer
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm


class CustomerForm(forms.ModelForm):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Please Enter valid alternate number. Up to 14 digits allowed.")
    alter_phone = forms.CharField(validators=[phone_regex],max_length=17, required=True, help_text='only number')
    class Meta:
        model = Customer
        fields = ['alter_phone','name','state','city' ,'locality','zipcode',]
        
class TempRegisterForm(forms.Form):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Please Enter valid number. Up to 14 digits allowed.")
    phone = forms.CharField(validators=[phone_regex],max_length=17, required=True, help_text='only number')
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = User.objects.filter(phone__iexact=phone)
        if qs.exists():
            raise forms.ValidationError("This Number is already Registered, Please Login")
        return phone

def validate_pass(value):
    if len(value) < 4:
        raise ValidationError('password must be contain 5 character')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone','password1','password2']


from django.contrib.auth import login,authenticate
class UserLoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    # clean() validation errors added to 'non_field_errors'
    def clean(self, *args, **kwargs):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')   
        if phone and password:
            query = User.objects.filter(phone__iexact = phone)
            if not query.exists():
                self.add_error('phone',"This Number is not Registred")
                #raise forms.ValidationError('This Number is not Registred')
            else:   
                user = authenticate(phone=phone, password=password)  
                if not user:
                    self.add_error('password',"Incorrect password. Please try again!")
                    #raise forms.ValidationError("Incorrect password. Please try again!")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone','name',)

    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user