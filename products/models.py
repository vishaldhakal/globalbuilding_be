from django.db import models 
from decimal import Decimal, ROUND_HALF_UP
import random
class Category(models.Model):
    name = models.CharField(max_length=100)  
    description = models.TextField(blank=True, null=True)  
    image = models.ImageField(upload_to="category_images/", blank=True, null=True) 
    parent = models.ForeignKey(
        'self',               
        null=True,          
        blank=True,          
        on_delete=models.CASCADE,  
        related_name='subcategories'  
    )

    def __str__(self):
        return self.name  
    
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,   
        related_name='products'    
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    hiked_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percent = models.PositiveIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True) 
    availability = models.BooleanField(default=True)             
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)
    description = models.TextField()  
    image = models.ImageField(upload_to='products/', blank=True)  

    def save(self, *args, **kwargs):
        # Random demo discount percent between 10 and 20
        discount_percent = Decimal(random.randint(10, 20))

        # Make sure price is Decimal
        price_decimal = Decimal(self.price)

        # Calculate hiked price
        self.hiked_price = (price_decimal / (Decimal('1.0') - discount_percent / Decimal('100'))).quantize(Decimal('0.01'))

        # Save the discount percent as well
        self.discount_percent = discount_percent

        # Random rating between 4.0 and 5.0
        self.rating = Decimal(random.uniform(4.0, 5.0)).quantize(Decimal('0.1'))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    products = models.ManyToManyField("Product", blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        product_names = ", ".join([p.name for p in self.products.all()])
        return f"Inquiry by {self.name} for {product_names}"