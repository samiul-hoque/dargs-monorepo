from django.contrib import admin

# Register your models here.
from dargs import models

admin.site.register(models.Class)
admin.site.register(models.Course)
admin.site.register(models.Room)
admin.site.register(models.School)
admin.site.register(models.Semester)
