from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm
from .models import Member


class MemberAdmin(UserAdmin):
    form = SignUpForm
    model = Member
    list_display = ["name", "username", "email", "user_img"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("name", "email", "user_img")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "name",
                    "user_img",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(Member, MemberAdmin)
