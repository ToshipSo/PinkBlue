from django.urls import path
from app.views import SignUpView, ProductListView, ProductCreateView, ProductApprove, ProductUpdateView, ApproveView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('products', ProductListView.as_view(), name='products'),
    path('create_product', ProductCreateView.as_view(), name='create_product'),
    path('approve_products', ApproveView.as_view(), name='approve_products'),
    path('update_product/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('api/approve/<int:pk>', ProductApprove.as_view(), name='approve'),
]
