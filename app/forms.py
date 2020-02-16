from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from app.models import CustomUser, ProductApproval


class CreateUserForm(UserCreationForm):
    choices = (
        (1, 'Store Assistant'),
        (2, 'Store Manager'),
    )
    role = forms.ChoiceField(choices=choices)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role')


class ProductCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProductCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        product = super(ProductCreateForm, self).save(commit=False)
        product.operation = 1
        product.user = self.request.user
        if commit:
            product.save()
        return product

    class Meta:
        model = ProductApproval
        fields = ('name', 'vendor', 'mrp', 'batch_no', 'batch_date', 'quantity')
