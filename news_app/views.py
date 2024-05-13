from django.views.generic import ListView
from django.shortcuts import redirect
from .models import News
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name="dispatch")
class NewsSearchView(ListView):
    model = News
    template_name = "news.html"
    context_object_name = 'news_items'
    paginate_by = 5
    
    def get_queryset(self):
        self.update_news()
        return News.objects.all().order_by("-created_at")

    def update_news(self):
        url = "https://tw.news.yahoo.com/archive/"
        response = requests.get(url)
        data = BeautifulSoup(response.text, "html.parser")
        titles = data.find_all("h3", class_="Mb(5px)")

        for title in titles:
            news_url = title.find("a", href=True)
            if news_url:
                full_url = news_url["href"]
                if not full_url.startswith("https"):
                    full_url = url + full_url

                if not News.objects.filter(url=full_url).exists():
                    source = requests.get(full_url)
                    source_data = BeautifulSoup(source.text, "html.parser")
                    source_name_tag = source_data.find("div", class_="source-info")
                    source_name = source_name_tag.text.strip() if source_name_tag else "出處不明！"
                    # 儲存進資料庫
                    News.objects.create(
                        title=title.text.strip(),
                        url=full_url,
                        source=source_name
                    )
