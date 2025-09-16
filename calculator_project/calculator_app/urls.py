from django.urls import path
from .views import CalculateAPIView, HistoryAPIView, index, calculator, history

urlpatterns = [
    path('', index, name='index'),
    path('calculator/', calculator, name='calculator'),
    path('history/', history, name='history'),
    path('api/calculate/', CalculateAPIView.as_view(), name='calculate-api'),
    path('api/history/', HistoryAPIView.as_view(), name='history-api'),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('calculate/', views.calculate_api_view, name='calculate'),
#     path('history/', views.history_api_view, name='history'),
# ]
