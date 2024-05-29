import time, datetime, os, requests, django
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import timezone
from news.models import News
from django.shortcuts import render

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

def news_list(request):
    news_items = News.objects.all().order_by("-created_at")[:20]
    return render(request, "pages/index.html", {"news_items":news_items})

def update_news():
    print("開始更新新聞...")
    url = "https://tw.news.yahoo.com/archive/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = BeautifulSoup(response.text, "html.parser")
            titles = data.find_all("h3", class_="Mb(5px)")
            print(f"找到 {len(titles)} 條新聞標題")
            for title in titles:
                news_url = title.find("a", href=True)
                if news_url:
                    full_url = news_url["href"]
                    if not full_url.startswith("https"):
                        full_url = url + full_url
                    if not News.objects.filter(url=full_url).exists():
                        try:
                            source = requests.get(full_url)
                            source_data = BeautifulSoup(source.text, "html.parser")
                            source_name_tag = source_data.find("div", class_="source-info")
                            source_name = source_name_tag.text.strip() if source_name_tag else "來源不明"
                            News.objects.create(
                                title=title.text.strip(),
                                url=full_url,
                                source=source_name,
                                created_at=timezone.now()
                            )
                            print(f"新聞 {title.text.strip()} 已保存。")
                        except Exception as e:
                            print(f"處理新聞URL發生錯誤：{e}")
        else:
            print("無法從網路取得資料。")
    except Exception as e:
        print(f"取得新聞列表發生錯誤{e}")   
    delete_three_day = timezone.now() - datetime.timedelta(days=3)
    old_news = News.objects.filter(created_at__lt=delete_three_day)
    count = old_news.count()
    old_news.delete()
    print(f"已刪除 {count} 條超過三天的資料！！！")
if __name__ == "__main__":
    try:
        while True:
            try:
                update_news()
                print("等待五分鐘...")
                time.sleep(60)
            except Exception as e:
                print(f"發生錯誤：{e}")
    except KeyboardInterrupt:
        print("手動中斷腳本！！！")
