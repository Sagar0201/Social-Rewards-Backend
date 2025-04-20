from django.contrib import admin
from .models import AppCategory,App,UserProfile,UserAppTask,AppSubCategory

# Register your models here.
admin.site.register(AppCategory)
admin.site.register(AppSubCategory)
admin.site.register(App)
admin.site.register(UserProfile)
admin.site.register(UserAppTask)