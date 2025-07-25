from django.db import models

class MotorcycleOrder(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    
    motorcycle_model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    frequency = models.CharField(max_length=50)  # Consider using choices
    additional_features = models.JSONField(blank=True, null=True)  # Use TextField if not using PostgreSQL

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.first_name} {self.last_name}"

class EmailList(models.Model):
    email:models.EmailField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email {self.id} is {self.email}"
