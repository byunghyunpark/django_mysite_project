from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser

# 기본으로 제공하는 UserCreationForm을 상속받아 사용
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'nickname', 'date_joined', 'phone_number', )
    list_filter = ('is_staff', )
    ordering = ('-date_joined', )
    readonly_fields = ('date_joined', )
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'nickname',
            )
        }),
        ('Personal Info', {
            'fields': (
                'last_name',
                'first_name',
                'phone_number',
            )
        }),
        ('Facebook Info', {
            'fields': (
                'is_facebook_user',
                'facebook_id',
                'img_profile_url',
            )
        }),
        ('Additional Info', {
            'fields': (
                'date_joined',
                'is_staff',
                'is_superuser',
            )
        }),
    )


    form = MyUserChangeForm
    add_form = MyUserCreationForm


admin.site.register(MyUser, MyUserAdmin)