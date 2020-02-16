from django.contrib import admin
from app.models import CustomUser, Product, ProductApproval

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(ProductApproval)
