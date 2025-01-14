from django.urls import path
from chat import views


urlpatterns = [
    path("<str:group_name>/", views.index, name="home"),
]
