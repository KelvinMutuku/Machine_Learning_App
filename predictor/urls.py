from django.urls import path
from .views import home, predict_view, predict_api

urlpatterns = [
    path("", home, name="home"),
    path("predict/", predict_view, name="predict"),
    path("api/predict/", predict_api, name="predict_api"),
]
