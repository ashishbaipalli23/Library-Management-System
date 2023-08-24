from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(User)
admin.site.register(StdProfile)
admin.site.register(TeacherProfile)
admin.site.register(BookAdd)
admin.site.register(BookRequest)
admin.site.register(Payment)