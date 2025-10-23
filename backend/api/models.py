from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Publisher(models.Model):
    name = models.CharField()
    country = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200, null=False, blank=False, error_messages={
            'blank': "Please enter a title, it cannot be empty.",
            'null': "Title is required.",
        })
    author = models.CharField(max_length=100, null=False, blank=False)
    published_year = models.DateField(null=False, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.published_year > timezone.now().date():
            raise ValidationError({'published_year': "Publication year cannot be in the future."})

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"{self.title}"


