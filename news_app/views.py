from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import redirect
from .models import News
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .news_reptile import update_news
from django.core.paginator import Paginator

@method_decorator(login_required, name="dispatch")
class NewsSearchView(ListView):
    model = News
    template_name = "news.html"
    context_object_name = "news_items"
    paginate_by = 5

    def get_queryset(self):
        update_news()
        return News.objects.all().order_by("-created_at")

def news_json(request):
    page_number = request.GET.get("page", 1) # 默認第一頁開始
    news_items = News.objects.all().order_by("-created_at") # 撈取所有資料倒敘顯示
    paginator = Paginator(news_items, 5)  # 5筆為一頁
    page_obj = paginator.get_page(page_number)

    data = {
        "news_item": list(page_obj.object_list.values("id", "title", "source", "url")),
        "has_previous": page_obj.has_previous(), # 是否有前一頁
        "has_next": page_obj.has_next(), # 是否有下一頁
        "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None, # 前一頁頁碼
        "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None, # 下一頁頁碼
        "current_page": page_obj.number, # 當前頁數
        "total_pages": paginator.num_pages # 總頁數
    }
    return JsonResponse(data) # 返回json格式