from django import forms
from gamestopapp.models import Product
from django.contrib.auth.models import User


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'manufacturer', 'price', 'category', 'isAvailable', 'image']
        exculde = []
        
        
class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'manufacturer', 'price', 'category', 'isAvailable']
        exculde = []
        
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    confirmPassword = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirmPassword']
        exculde = []
        
class UserLoginForm(forms.Form):
    password = forms.CharField(widget= forms.PasswordInput)
    username = forms.CharField(max_length= 200)
     

class UpdateUserForm(forms.Form):
    first_name = forms.CharField(max_length= 200)
    last_name = forms.CharField(max_length= 200)
    username = forms.CharField(max_length= 200)
    email = forms.EmailField(max_length= 200)
    is_staff = forms.BooleanField()
    
    

    