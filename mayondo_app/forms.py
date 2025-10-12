from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Sale, Product,CustomUser
from django.contrib.auth.models import User
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
    # error_messages = {
    #         'Customer_name': {'required': 'Customer name is required.'},
    #         'Product_type': {'required': 'Please select a product type.'},
    #         'Product': {'required': 'Please select a product name.'},
    #         'Quantity': {'required': 'Please enter the quantity sold.'},
    #         'payment_type': {'required': 'Please select a payment method.'},
    #         'Transport_included': {'required': 'Please select a transport method.'},
    #         'Sales_agent': {'required': 'Sales agent name is required.'},
    #     }

    # def clean_Paid_amount(self):
    #     paid_amount = self.cleaned_data['Paid_amount']
    #     if paid_amount is None:
    #         raise forms.ValidationError("Paid amount should not be left empty.")
    #     elif paid_amount <= 0:
    #         raise forms.ValidationError("Please enter amount above 0.")
    #     return paid_amount

    # def clean_Product_name(self):
    #     product_name = self.cleaned_data['Product_name']
    #     if not product_name:
    #         raise forms.ValidationError("Please select a product.")
    #     return product_name


    # def clean_Quantity(self):
    #     quantity = self.cleaned_data['Quantity']
    #     if quantity <= 0:
    #         raise forms.ValidationError("Please enter quantity above 0.")
    #     return quantity

    # def clean_Unit_cost(self):
    #     unit_cost = self.cleaned_data['Unit_cost']
    #     if unit_cost is None or unit_cost <= 0:
    #         raise forms.ValidationError("Please enter cost above 0.")
    #     return unit_cost

    

    # def clean_Total_amount(self):
    #     total_amount = self.cleaned_data['Total_amount']
    #     paid_amount = self.cleaned_data.get('Paid_amount')
    #     if total_amount is None:
    #         raise forms.ValidationError("Total amount is required.") 
    #     if total_amount <= 0:  
    #         raise forms.ValidationError("Please enter amount above 0.")
    #     elif paid_amount and total_amount < paid_amount:
    #         raise forms.ValidationError("Total amount must be equal to or more than paid amount.")
    #     return total_amount

    # def clean_Customer_name(self):
    #     customer_name = self.cleaned_data['Customer_name']
    #     if not customer_name:
    #         raise forms.ValidationError("Customer name cannot be empty.")
    #     elif customer_name.isdigit():
    #         raise forms.ValidationError("Customer name cannot be entirely numeric.")
    #     return customer_name

    # def clean_Sales_agent(self):
    #     sales_agent = self.cleaned_data['Sales_agent']
    #     if not sales_agent:
    #         raise forms.ValidationError("Sales agent name cannot be empty.")
    #     elif sales_agent.isdigit():
    #         raise forms.ValidationError("Sales agent name cannot be entirely numeric.")
    #     return sales_agent

    # def clean_Product_type(self):
    #     product_type = self.cleaned_data['Product_type']
    #     if not product_type:
    #         raise forms.ValidationError("Product type cannot be empty.")
    #     elif product_type.isdigit():
    #         raise forms.ValidationError("Product type cannot be entirely numeric.")
    #     return product_type

    # def clean_Method_of_payment(self):
    #     method_of_payment = self.cleaned_data['Method_of_payment']
    #     if not method_of_payment:
    #         raise forms.ValidationError("Please select a payment method.")
    #     return method_of_payment

    # def clean_Transport_included(self):
    #     transport_included = self.cleaned_data['Transport_included']
    #     if not transport_included:
    #         raise forms.ValidationError("Please click if transport_included.")
    #     return transport_included

     




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


# class LoginAuthenticationForm(AuthenticationForm):
#     error_messages = {
#         'invalid_login': "please check your credentials and try again"
#     }
#     username = forms.CharField(error_messages={"required": "please enter the username"})
#     password = forms.CharField(error_messages={"required": "please enter the password"})
class LoginAuthenticationForm(AuthenticationForm):
    username = forms.CharField(error_messages={"required": "please enter the username"})
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        error_messages={"required": "please enter the password"}
    )
    error_messages = {
        'invalid_login': "please check your credentials and try again"
    }






