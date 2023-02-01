from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model


CustomUser = get_user_model()
admin.site.register(CustomUser)
