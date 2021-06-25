from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUser(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'direction', 'date_of_birth')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'direction', 'date_of_birth')}),
    )


admin.site.register(User, CustomUser)
