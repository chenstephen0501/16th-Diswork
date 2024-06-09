from django.shortcuts import render
from .models import Ads


def ads_processor(request):
    try:
        ads = Ads.objects.all()
        is_iterable = True
    except Exception as e:
        ads = None
        is_iterable = False
    return {"ads": ads, "is_iterable": is_iterable}
