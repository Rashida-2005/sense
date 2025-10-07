from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Sale, Product,CustomUser,Employee
from django.contrib.auth.models import User

# Sale Form 
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            'customer_name',
            'product_type',
            'product',
            'quantity',
            'sale_date',
            'payment_type',
            'sales_agent',
            'transport_included',
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'border rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-indigo-500 focus:outline-none'}),
            'quantity': forms.NumberInput(attrs={'class': 'border rounded-lg px-5 py-4 w-full focus:ring-2 focus:ring-indigo-500 focus:outline-none','placeholder': 'Enter quantity'}),
            'sale_date': forms.DateInput(attrs={'type': 'date','class': 'border rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-indigo-500 focus:outline-none'}),
            'payment_type': forms.Select(choices=[
                ('cash', 'Cash'),
                ('cheque', 'Cheque'),
                ('bank_overdraft', 'Bank Overdraft'),
            ]),
            'transport_included': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 rounded'}),
        }


#widget will let me control my html represatation of form fiel(styling,behavior and attributes)
# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # This will include all model fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full', 'placeholder': 'Enter product name'}),
            'type': forms.Select(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'supplier_name': forms.TextInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'cost_price': forms.NumberInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'product_price': forms.NumberInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'quality': forms.TextInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'color': forms.TextInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'measurement': forms.TextInput(attrs={'class': 'border rounded-lg px-3 py-2 w-full'}),
            'date_added': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded-lg px-3 py-2 w-full'}),
        }
        error_messages = {
            "name": {"required": "please enter the product name"},
            "type": {"required": "please select the product type"},
            "supplier_name": {"required": "please enter the supplier's name"},
            "product_price": {"required": "please enter the product price"},
            "date_added": {"required": "please enter the date"}}
        
# Register Form
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username","email", "password1", "password2", "role"]
    username = forms.CharField(error_messages={"required": "please enter the username"})
    email = forms.EmailField(error_messages={"required": "please enter your email"})
    password1 = forms.CharField(error_messages={"required": "please enter your password"})
    password2 = forms.CharField(error_messages={"required": "please confirm your password"})


class LoginAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "please check your credentials and try again"
    }
username = forms.CharField(error_messages={"required": "please enter the username"})
password = forms.CharField(error_messages={"required": "please enter the password"})
  


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'position', 'salary', 'date_joined', 'is_active']
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }


