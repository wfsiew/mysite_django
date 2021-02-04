from django.db import models

# Create your models here.
class Product(models.Model):
    
    class Meta:
        db_table = 'product'
        
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=200)
    
class Order(models.Model):
    
    class Meta:
        db_table = 'order'
        
    name = models.CharField(max_length=300)
    line1 = models.CharField(max_length=300)
    line2 = models.CharField(max_length=300, blank=True, null=True)
    line3 = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=200)
    giftwrap = models.BooleanField()
    shipped = models.BooleanField()
    
class CartLine(models.Model):
    
    class Meta:
        db_table = 'cartline'
        
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartline_product', db_column='product_id')
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cartline_order', db_column='order_id')
    