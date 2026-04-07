from django.db import models

from users.models import User

SUPPLEMENT_TYPES = [
    ('Protein', 'Protein'),
    ('Creatine', 'Creatine'),
    ('Vitamin', 'Vitamin'),
    ('Pre Workout', 'Pre Workout'),
    ('Fat Burner', 'Fat Burner'),
    ('Gainers', 'Gainers'),
    ('Amino Acids', 'Amino Acids'),
    ('Collagen', 'Collagen'),
    ('Testosteron Booster', 'Testosteron Booster'),
    ('Accessories', 'Accessories'),
    ('Weight Loss', 'Weight Loss'),
]

class Product(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=SUPPLEMENT_TYPES)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    weight = models.FloatField(help_text="in grams/kilograms", null=True, blank=True)
    flavor = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    discount_percent = models.IntegerField(null=True, blank=True)

    def get_discount_percentage(self):
        if self.discount_price:
            return int(100 - (self.discount_price / self.price * 100))
        return 0

    def get_discount_price(self):
        if self.discount_percent:
            return self.price - (self.price * self.discount_percent / 100)
        return self.price

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Shiko'),
        ('shipped', 'Në rrugë'),
        ('delivered', 'Marrë'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"