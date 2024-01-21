from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Dweet, Comment, DweetCategory


class profileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "email", "first_name"]
    inlines = [profileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Dweet)
admin.site.register(Comment)
admin.site.register(DweetCategory)
# admin.site.register(Profile)

# Register your models here.
