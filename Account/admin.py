from django.contrib import admin
from Account.models import ModelUsers, CustomUser
# Register your models here.


admin.site.register(ModelUsers)
admin.site.register(CustomUser)