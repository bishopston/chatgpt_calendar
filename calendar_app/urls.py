from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_calendar, name='calendar'),
    path('<int:year>/<int:month>/', views.display_calendar, name='calendar_month'),
]
