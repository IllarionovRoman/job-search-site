from django.contrib import admin
from .models import Employees, Category, Person
# Register your models here.

admin.site.register(Employees)
admin.site.register(Category)
admin.site.register(Person)

