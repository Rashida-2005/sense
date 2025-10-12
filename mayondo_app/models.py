from django.db import models
# Create your models here.
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.core.exceptions import ValidationError 

# Optional: Extend User with a profile model if you want roles
class CustomUser(AbstractUser):
      ROLES = [('user', 'User'),('admin', 'Admin'),('manager', 'Manager')]
      role = models.CharField(max_length=50, choices=ROLES, unique=False)

      def __str__(self):
        return self.username


# Product Model
class Product(models.Model):
    PRODUCT_TYPES = [
        ('wood', 'Wood'),
        ('furniture', 'Furniture'),
    ]
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    supplier_name = models.CharField(max_length=200)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.PositiveIntegerField(default=0)
    quality = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    measurement = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} ({self.type})"
    class Meta:
        ordering = ['-date_added']



# class Sale(models.Model):
#     customer_name = models.CharField(max_length=255)
#     product_type = models.CharField(max_length=100)
#     product = models.ForeignKey("Product", on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     sale_date = models.DateTimeField(default=now)
#     payment_type = models.CharField(
#         max_length=20,
#         choices=[
#             ('cash', 'Cash'),
#             ('cheque', 'Cheque'),
#             ('bank_overdraft', 'Bank Overdraft'),
#         ]
#     )
#     sales_agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
#     transport_included = models.BooleanField(default=False)
#     total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

#     def __str__(self):
#         return f"Sale #{self.id} - {self.customer_name} ({self.product.name}) x{self.quantity}"

#     # Helper methods (calculation only, not stored in DB)
#     def subtotal(self):
#         return self.product.product_price * Decimal(self.quantity) if self.product else 0

#     def transport_fee(self):
#         return self.subtotal() * Decimal("0.05") if self.transport_included else 0

#     def total_price(self):
#         return self.subtotal() + self.transport_fee()

#     # Override save (store total + reduce stock safely)
#     def save(self, *args, **kwargs):
#         # Always recalculate total
#         self.total = self.total_price()

#         # Reduce stock only if it's a NEW sale
#         if not self.pk:
#             if self.product.stock_quantity < self.quantity:
#                 raise ValueError("Not enough stock to complete this sale.")
#             self.product.stock_quantity -= self.quantity
#             self.product.save()

#         super().save(*args, **kwargs)

#     class Meta:
#         ordering = ['-sale_date']
 
                


class Sale(models.Model):
    customer_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(default=now)
    payment_type = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('bank_overdraft', 'Bank Overdraft'),
        ]
    )
    sales_agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    transport_included = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Sale #{self.id} - {self.customer_name} ({self.product.name}) x{self.quantity}"

    # ✅ Prevent future sales
    def clean(self):
        if self.sale_date > now():
            raise ValidationError("Sale date cannot be in the future.")

    def subtotal(self):
        return self.product.product_price * Decimal(self.quantity) if self.product else 0

    def transport_fee(self):
        return self.subtotal() * Decimal("0.05") if self.transport_included else 0

    def total_price(self):
        return self.subtotal() + self.transport_fee()

    # ✅ Call clean() before save()
    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation checks are applied

        self.total = self.total_price()

        if not self.pk:  # New sale
            if self.product.stock_quantity < self.quantity:
                raise ValueError("Not enough stock to complete this sale.")
            self.product.stock_quantity -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-sale_date']

  
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_joined = models.DateField(default=now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"

