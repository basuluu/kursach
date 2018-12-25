from django.db import models
from django.utils import timezone

class product_card(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50)
    item_section = models.CharField(max_length=50)
    item_country = models.CharField(max_length=30)
    item_barcode = models.CharField(max_length=12)
    item_cost = models.IntegerField()
    item_number = models.IntegerField()
    item_photo = models.ImageField(upload_to='images/', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    vision = models.BooleanField(default=False)

class bin(models.Model):
    id = models.AutoField(primary_key=True)
    id_item = models.ForeignKey('product_card', on_delete=models.CASCADE)
    num = models.IntegerField()

class user_bin(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    id_bin = models.ForeignKey('bin', on_delete=models.CASCADE)
    pay_status = models.BooleanField(default=False)

class journal_request(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    name = models.CharField(max_length=16)
    address = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

class req_bin(models.Model):
    id_req = models.ForeignKey('journal_request', on_delete=models.CASCADE)
    id_bin = models.ForeignKey('bin', on_delete=models.CASCADE)

class journal_supplier(models.Model):
    sup_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    category = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

class income(models.Model):
    date = models.DateTimeField()
    sup = models.CharField(max_length=30)
    item = models.CharField(max_length=30)
    num = models.IntegerField()
