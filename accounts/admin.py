from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth.forms import UserChangeForm as _UserChangeForm

class UserChangeForm(_UserChangeForm):
    class Meta(_UserChangeForm.Meta):
        model = User

class UserAdmin(_UserAdmin):
    form = UserChangeForm

    fieldsets = _UserAdmin.fieldsets + (
            (None, {'fields': ('last_track_pull',)}),
    )


admin.site.register(User, UserAdmin)