from django.urls import path

from . import views

urlpatterns = [
  path('artikel/', views.cariArtikelScholar),
  path('artikel-google/', views.scrape_google),
  path('ekstrak/', views.ekstrak),
  # path('tes/', views.TodoListView.as_view()),
  # path('todos/<int:id>/', views.TodoListView.as_view()),
]