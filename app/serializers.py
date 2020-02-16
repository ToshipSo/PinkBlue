from rest_framework.serializers import ModelSerializer
from .models import Product, ProductApproval


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductApprovalSerializer(ModelSerializer):
    class Meta:
        model = ProductApproval
        fields = ('name', 'vendor', 'mrp', 'batch_no', 'batch_date', 'quantity')
