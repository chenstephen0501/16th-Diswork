from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Member


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        label="姓名",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    email = forms.EmailField(
        label="信箱",
        widget=forms.EmailInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )

    class Meta:
        model = Member
        fields = ("name", "username", "email", "password1", "password2", "user_img")

    # 2024/5/9 增加 -- Jeter
    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     if not email.endswith("@gmail.com"):
    #         raise forms.ValidationError("只接受 Gmail 格式註冊，請使用 Gmail 作為您的信箱。")
    #     return email
    def clean_email(self):
        email = self.cleaned_data["email"]
        allowed_domains = ["gmail.com", "yahoo.com.tw", "outlook.com"]
        email_domain = email.split("@")[-1]
        if email_domain not in allowed_domains:
            allowed_domains_str = ", ".join(allowed_domains)
            raise forms.ValidationError(
                f"只接受以下域名的郵箱註冊：{allowed_domains_str}。"
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
