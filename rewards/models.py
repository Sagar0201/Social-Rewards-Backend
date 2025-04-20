from django.db import models
from django.contrib.auth.models import User

class AppCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class AppSubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(AppCategory, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class App(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='app_logos/')
    app_link = models.URLField()
    category = models.ForeignKey(AppCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(AppSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    points = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    
    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return None
    

        
        
        
        
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.user.username   
    

class UserAppTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='task_screenshots/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'app')
    
    def __str__(self):
        return f"{self.user.username} - {self.app.name}"