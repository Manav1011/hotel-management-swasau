
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group
from .models import CustomUser
from .forms import CustomUserCreationForm,CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('email','is_staff','is_active')
    list_filter = ('email','is_staff','is_active')

    fieldsets = (
        (None, {
            "fields": (
                'email','password',
            ),
        }),('Permissions',{
            'fields':('is_staff','is_active')
        })
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    search_fields = ('email',)    
    ordering = ('email',)    

admin.site.unregister(Group)
admin.site.register(CustomUser,CustomUserAdmin)
