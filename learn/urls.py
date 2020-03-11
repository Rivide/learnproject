from django.urls import path
from . import views


urlpatterns = [
    path('', views.LanguageListView.as_view(), name='index'),
    path('subject/<str:subject>/', views.UnitNodeListView.as_view(), name='unit_list'),
    path('subject/<str:subject>/<str:course>/', views.UnitNodeListView.as_view(), name='unit'),
    path('practice/<str:title>/<int:practice>/', views.practice, name='practice'),
    path('practice/<str:title>/<int:practice>/<int:question>/', views.question_view, name='question'),
    path('article/read/<str:title>/', views.ArticleDetailView.as_view(),
         name='article'),
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/update/<str:title>/', views.ArticleUpdateView.as_view(), name='article_update')
    # path('create/', views.question_create, name='question_create')
]