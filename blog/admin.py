from django.contrib import admin
from .models import Topics, Comments, Encouragements

# Register your models here.

admin.site.register(Topics)
admin.site.register(Comments)
admin.site.register(Encouragements)
