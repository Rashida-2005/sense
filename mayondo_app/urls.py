from django.contrib import admin
from django.urls import path,include
from mayondo_app.views import receipt_view,loginpage,registerpage,product_deletepage,logoutpage,landing,dashboardpage,product_listpage,product_createpage,product_editpage,sales_listpage,stock_reportpage,sale_createpage,sales_reportpage,sale_createpage,sale_editpage,sale_deletepage


app_name = 'mayondo_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing, name='landing'),
    path('login/',loginpage, name='login'),
    path('register/',registerpage, name='register'),
    path('logout/',logoutpage, name='logout'),
    path('dashboard/',dashboardpage, name='dashboard'),
    # path('user-dashboard/',user_dashboardpage, name='user_dashboard'),

    path('products/',product_listpage, name='product_list'),
    path('products/new/',product_createpage, name='product_create'),
    path('products/<int:pk>/edit/',product_editpage, name='product_edit'),
    path('products/delete/<int:pk>/',product_deletepage, name='delete_product'),
    path('sales/',sales_listpage, name='sales_listpage'),
    path('sales/new/',sale_createpage, name='sale_create'),
    path('sales/<int:pk>/edit/', sale_editpage, name="sale_edit"),
    path('sales/<int:pk>/delete/', sale_deletepage, name="sale_delete"),

    path('reports/stock/',stock_reportpage, name='stock_report'),
    path('reports/sales/',sales_reportpage, name='sales_report'),
    path('receipt/<int:sale_id>/', receipt_view, name='receipt'),

        
]