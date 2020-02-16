from django.shortcuts import render
from django.views.generic import CreateView, ListView, View
from .forms import CreateUserForm, ProductCreateForm
from .models import Product, ProductApproval
from .serializers import ProductSerializer, ProductApprovalSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class SignUpView(CreateView):
    form_class = CreateUserForm
    template_name = 'registration/signup.html'
    success_url = '/products'


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products.html'
    context_object_name = 'approved_products'


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ProductCreateView(PassRequestToFormViewMixin, CreateView):
    form_class = ProductCreateForm
    template_name = 'product_create.html'
    success_url = '/products'


class ApproveView(ListView):
    queryset = ProductApproval.objects.all()
    template_name = 'products.html'
    context_object_name = 'products'


class ProductUpdateView(View):

    def get(self, request, pk, *args, **kwargs):
        context = {
            'product': Product.objects.filter(pk=pk).first()
        }
        return render(request, 'product_create.html', context)


class ProductApprove(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductApprovalSerializer

    def put(self, request, *args, **kwargs):
        if request.user.role == 2:
            ProductApproval.objects.filter(pk=kwargs['pk']).update(user=request.user)
            ProductApproval.objects.filter(pk=kwargs['pk']).first().save()
            return Response({
                'status': 'Approved'
            })
        else:
            return Response({
                'status': 'Not Authorized'
            })


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        data = request.data
        p = ProductApproval(name=data['name'], vendor=data['vendor'], mrp=data['mrp'], batch_no=data['batch_no'],
                            batch_date=data['batch_date'], quantity=data['quantity'], operation=2, user=request.user)
        p.change_id = kwargs['pk']
        p.save()
        response = 'Updated' if request.user.role == 2 else 'Sent for Approval'
        return Response({
            'status': response
        })

    def create(self, request, *args, **kwargs):
        data = request.data
        p = ProductApproval(name=data['name'], vendor=data['vendor'], mrp=data['mrp'], batch_no=data['batch_no'],
                            batch_date=data['batch_date'], quantity=data['quantity'], operation=1, user=request.user)
        p.save()
        response = 'Created' if request.user.role == 2 else 'Sent for Approval'
        return Response({
            'status': response
        })

    def destroy(self, request, *args, **kwargs):
        data = request.data
        p = ProductApproval(name='NA', vendor='NA', mrp=0, batch_no=0, batch_date='2000-01-01', quantity=0,
                            change_id=kwargs['pk'], operation=3, user=request.user)
        p.save()
        response = 'Deleted' if request.user.role == 2 else 'Sent for Approval'
        return Response({
            'status': response
        })
