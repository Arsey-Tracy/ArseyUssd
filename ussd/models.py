from django.db import models


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)


class Transporter(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)


class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)
    details = models.TextField()
    status = models.CharField(max_length=50, default="Pending")


class Role(models.Model):
    ROLE_CHOICES = (
        (' vendor', ' Vendor'),
        (' transporter', ' Transporter')
    )
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
