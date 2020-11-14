from django.db import models


class ProductModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=30)
    img = models.ImageField(upload_to='product_images/')
    details_description = models.CharField(max_length=10000, blank=True)


class UserModel(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.IntegerField()
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    email = models.EmailField(primary_key=True, max_length=30)
    password = models.CharField(max_length=30)


class BillModel(models.Model):
    email = models.EmailField(max_length=30)
    name = models.CharField(max_length=30)
    products_quantity = models.IntegerField()
    actual_price = models.IntegerField()
    discounted = models.IntegerField()
    total_bill = models.IntegerField()


class CartModel(models.Model):
    email = models.CharField(max_length=30)
    pid = models.IntegerField()
