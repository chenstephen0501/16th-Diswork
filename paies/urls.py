from django.urls import path
from . import views

app_name = 'paies'

urlpatterns = [
    # 路由: /
    path('', views.index, name='index'),
    
    # 路由: /createOrder
    path('createOrder', views.create_order, name='create_order'),
    
    # 路由: /check/<id>
    path('check/<int:TimeStamp>', views.check_order, name='check_order'),
    
    # 路由: /newebpay_return
    path('newebpays_return', views.newebpay_return, name='newebpay_return'),
    
    # 路由: /newebpay_notify
    path('newebpays_notify', views.newebpay_notify, name='newebpay_notify'),
]
