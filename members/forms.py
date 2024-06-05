from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        label="暱稱",
        widget=forms.TextInput(
            attrs={
                "class": "p-2 border-2 border-gray-300 w-full",
                "placeholder": "請輸入暱稱",
            }
        ),
    )
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(
            attrs={
                "class": "p-2 border-2 border-gray-300 w-full",
                "placeholder": "請輸入帳號",
            }
        ),
    )
    email = forms.CharField(
        label="信箱",
        widget=forms.EmailInput(
            attrs={
                "class": "p-2 border-2 border-gray-300 w-full",
                "placeholder": "請輸入信箱",
            }
        ),
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(
            attrs={
                "class": "p-2 border-2 border-gray-300 w-full",
                "placeholder": "請輸入密碼",
            }
        ),
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(
            attrs={
                "class": "p-2 border-2 border-gray-300 w-full",
                "placeholder": "確認密碼",
            }
        ),
    )

    class Meta:
        model = Member
        fields = ("name", "username", "email", "password1", "password2", "user_img")

    def clean_email(self):
        email = self.cleaned_data["email"]
        allowed_domains = ["gmail.com", "yahoo.com.tw", "outlook.com"]
        email_domain = email.split("@")[-1]
        if email_domain not in allowed_domains:
            allowed_domains_str = ", ".join(allowed_domains)
            raise forms.ValidationError(
                f"只接受以下信箱進行註冊：{allowed_domains_str}。"
            )
        return email


class MemberUpdateForm(UserChangeForm):
    name = forms.CharField(
        label="姓名：",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    username = forms.CharField(
        label="帳號：",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    email = forms.EmailField(
        label="信箱：",
        widget=forms.EmailInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    user_img = forms.ImageField(label="上傳頭貼")
    password = None

    class Meta:
        model = Member
        fields = ("name", "username", "email", "user_img")
