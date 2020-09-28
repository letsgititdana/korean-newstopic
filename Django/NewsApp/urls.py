from django.urls import path
from.import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('news2020/', views.news2020, name='news2020'),
    path('news2019/', views.news2019, name='news2019'),
    path('news2018/', views.news2018, name='news2018'),
    path('news2017/', views.news2017, name='news2017'),
    path('articles/', views.articles, name='articles'),
    path('articles/<article_id>/', views.articles),
]
