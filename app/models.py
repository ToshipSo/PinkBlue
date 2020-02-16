from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_TYPE = (
        (1, 'Store Assistant'),
        (2, 'Store Manager'),
    )
    email = models.EmailField(max_length=254, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_TYPE, default=2)


class Product(models.Model):
    STATUS = (
        (1, 'Approved'),
        (2, 'Create'),
        (3, 'Update'),
        (4, 'Delete'),
    )
    name = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    mrp = models.FloatField()
    batch_no = models.IntegerField()
    batch_date = models.DateField()
    quantity = models.IntegerField()


class ProductApproval(models.Model):
    STATUS = (
        (1, 'Create'),
        (2, 'Update'),
        (3, 'Delete'),
    )
    change_id = models.IntegerField(null=True)
    operation = models.PositiveSmallIntegerField(choices=STATUS)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    mrp = models.FloatField()
    batch_no = models.IntegerField()
    batch_date = models.DateField()
    quantity = models.IntegerField()


@receiver(signals.post_save, sender=ProductApproval)
def move_product(sender, instance, created, **kwargs):
    if instance.user.role == 2:
        if instance.operation == 1:
            product = Product(name=instance.name, vendor=instance.vendor, mrp=instance.mrp, batch_no=instance.batch_no,
                              batch_date=instance.batch_date, quantity=instance.quantity)
            product.save()
        elif instance.operation == 2:
            product = Product.objects.filter(pk=instance.change_id)
            product.update(name=instance.name, vendor=instance.vendor, mrp=instance.mrp, batch_no=instance.batch_no,
                           batch_date=instance.batch_date, quantity=instance.quantity)
        elif instance.operation == 3:
            Product.objects.filter(pk=instance.change_id).delete()
        ProductApproval.objects.filter(pk=instance.pk).delete()
