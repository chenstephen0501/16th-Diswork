from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    title = forms.CharField(
        label="看板",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300 w-full"}),
    )
    rule = forms.CharField(
        label="版規",
        widget=forms.TextInput(
            attrs={"class": "mx-1 border-2 border-gray-300 h-32 w-full"}
        ),
    )

    class Meta:
        model = Category
        fields = ["title", "rule", "status"]
        labels = {
            "title": "看板",
            "rule": "板規",
            "status": "看板狀態",
        }
