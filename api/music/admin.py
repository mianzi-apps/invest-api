from django.contrib import admin
from .models import Songs

# Register your models here.
# to ensure usage in the admin panel

admin.site.register(Songs)