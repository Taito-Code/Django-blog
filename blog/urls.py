from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("new/",views.new, name="new"),
  path("article/tech/", views.tech_all, name="tech_all"),
  path("article/life/", views.life_all, name="life_all"),
  path("abount/", views.about, name="about"),
  path("contact/", views.contact, name="contact"),
  path("article/all/", views.article_all, name="article_all"),
  path("article/<int:pk>/", views.view_article, name="view_article"),
  path("article/<int:pk>/edit/", views.edit, name="edit"),
  path("article/<int:pk>/delete/",views.delete,name="delete"),
  path('article/<int:pk>/ine_ajax/', views.add_ine, name='ine'),
]