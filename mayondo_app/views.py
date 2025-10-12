from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, get_user_model,logout
from decimal import Decimal
from .models import Product,Sale,Employee,CustomUser
from mayondo_app.forms import ProductForm,SaleForm,RegisterForm
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,LoginAuthenticationForm 
from .decorators import role_required
User = get_user_model()



def landing(request):
    return render(request, 'index.html')

# Logout view
def logoutpage(request):
    logout(request)
    return render(request,'logout.html')

# @login_required(login_url='mayondo_app:login')
def dashboardpage(request):
    user = request.user
    role = getattr(user, 'role', 'user').lower()  # normalize role

    # Everyone can see all products
    products = Product.objects.all()
    # Admins and managers see all sales, users see only their own
    sales = Sale.objects.all() if role in ['manager', 'admin'] else Sale.objects.filter(sales_agent=user)
    # Employees list only for managers
    employees = User.objects.all() if role == 'manager' else None

    # Chart & stats
    product_names = list(products.values_list('name', flat=True))
    product_sales = [sales.filter(product=p).aggregate(total=Sum('quantity'))['total'] or 0 for p in products]
    product_stock = list(products.values_list('stock_quantity', flat=True))

    total_products = products.count()
    total_sales = sales.count()
    total_stock = products.aggregate(total=Sum('stock_quantity'))['total'] or 0
    top_product = sales.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold').first()
    employees_count = employees.count() if employees else 0

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
        'product_names': product_names,
        'product_sales': product_sales,
        'product_stock': product_stock,
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

# Login page view
# def loginpage(request):
#     if request.method == 'POST':
#         identifier = request.POST.get("identifier")
#         password = request.POST.get("password")

#         # Try authenticating by username
#         user = authenticate(request, username=identifier, password=password)

#         # If username fails, try email
#         if user is None:
#             try:
#                 user_obj = User.objects.get(email=identifier)
#                 user = authenticate(request, username=user_obj.username, password=password)
#             except User.DoesNotExist:
#                 user = None

#         if user is not None:
#             login(request, user)
#          # Redirect based on role
#             role = getattr(user, 'role', 'user').lower()
#             if role in ["manager", "admin"]:
#                 return redirect("mayondo_app:dashboard")
#         messages.error(request, "Invalid credentials")
#         return redirect("mayondo_app:login")
#     form = LoginAuthenticationForm()
#     return render(request, "login.html", {"form": form})

def loginpage(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        # Try authenticate by username first
        user = authenticate(request, username=identifier, password=password)

        # If username fails, try email
        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            # Redirect everyone to dashboard
            return redirect("mayondo_app:dashboard")

        # If authentication failed
        messages.error(request, "Invalid credentials")
        return redirect("mayondo_app:login")

    # GET request
    form = LoginAuthenticationForm()
    return render(request, "login.html", {"form": form})

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
