from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, get_user_model,logout
from decimal import Decimal
from .models import Product,Sale,Employee,CustomUser
from mayondo_app.forms import ProductForm,SaleForm,RegisterForm,EmployeeForm
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,LoginAuthenticationForm 
User = get_user_model()


def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mayondo_app:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

def employee_editpage(request, pk):
    Employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=Employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=Employee)
    
    return render(request, 'employee_form.html', {'form': form, 'product': Employee})

def employee_delete(request, pk):
    try:
        employee = CustomUser.objects.get(pk=pk)
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Employee not found.")
    return redirect("mayondo_app:employee_list")
def employee_list(request):
    users = CustomUser.objects.all()
    return render(request, "employee_list.html", {"users": users})

#landing page
def landing(request):
    return render(request, 'index.html')

# Logout view
def logoutpage(request):
    logout(request)
    return render(request,'logout.html')



# @login_required(login_url='mayondo_app:login')
def dashboardpage(request):
    user = request.user
    role = getattr(user, 'role', 'user')
    
    products = Product.objects.none()
    sales = Sale.objects.none()
    employees = CustomUser.objects.all()

    # Safely get role
    if hasattr(user, 'role'):
        role = user.role

    # Query products and sales based on role
    if role == "manager":
        products = Product.objects.all()
        sales = Sale.objects.all()
    else:
        products = Product.objects.all()
        sales = Sale.objects.all()

    # Aggregated stats
    total_products = products.count()
    total_sales = sales.count()
    total_stock = products.aggregate(total=Sum('stock_quantity'))['total'] or 0

    top_product = sales.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold').first()
    employees_count = CustomUser.objects.count()  # if you track employees in your custom user model

    context = {
        'role': role,
        'total_products': total_products,
        'total_sales': total_sales,
        'total_stock': total_stock,
        'top_product': top_product['product__name'] if top_product else None,
        'top_product_quantity': top_product['total_sold'] if top_product else 0,
        'employees_count': employees_count,
        'products': products,
        'sales': sales,
        'employees': employees,
    }
    return render(request, 'dashboard.html', context)
 




# Product Views
def product_listpage(request):
    products = Product.objects.all().order_by('-date_added')
    context = {'products': products}
    return render(request, 'product_list.html', context)


def product_createpage(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mayondo_app:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})


def product_editpage(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('mayondo_app:product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'product': product})
 
def product_deletepage(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('mayondo_app:product_list')


    
# Sale Views
def sales_listpage(request):
    sales = Sale.objects.all().order_by('-sale_date')
    return render(request, 'sales_list.html', {'sales': sales})

def sale_createpage(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.save()  # model handles total + stock reduction
            return redirect('mayondo_app:sales_listpage')
    else:
        form = SaleForm()
    return render(request, 'sales_form.html', {'form': form})

def sale_editpage(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("mayondo_app:sales_listpage")
    else:
        form = SaleForm(instance=sale)
    return render(request, "sales_form.html", {"form": form})


def sale_deletepage(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect("mayondo_app:sales_listpage")

# Reports
def stock_reportpage(request):
    products = Product.objects.all()

    for product in products:
        sold_qty = Sale.objects.filter(product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0
        product.remaining_stock = product.stock_quantity - sold_qty  # if you want to keep original stock_quantity as total
        # OR if stock_quantity is already updated, just use product.stock_quantity directly

    low_stock = products.filter(stock_quantity__lt=5)

    return render(request, 'stock_report.html', {
        'products': products,
        'low_stock': low_stock
    })


def sales_reportpage(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sales = Sale.objects.all()

    if start_date and end_date:
        sales = sales.filter(sale_date__range=[start_date, end_date])

    total_sales_value = sales.aggregate(Sum('total'))['total__sum'] or 0

    return render(request, 'sales_report.html', {
        'sales': sales,
        'total_sales_value': total_sales_value,
    })


def receipt_view(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    context = {"sale": sale}
    return render(request, "receipt.html", context)


def loginpage(request):
    if request.method == 'POST':
        form = LoginAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('mayondo_app:dashboard')
        else:
            print(form.errors)
    else:  
        form = LoginAuthenticationForm()
    context = {"form": form}
    return render(request, "login.html", context)

def registerpage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mayondo_app:login')
        
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)
