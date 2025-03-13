from django.contrib import admin
from django.contrib.auth.models import Group 
from .models import CustomUser, Tweet

#Unregister Groups
admin.site.unregister(Group)


#Registering profile:
admin.site.register(CustomUser)
admin.site.register(Tweet)


