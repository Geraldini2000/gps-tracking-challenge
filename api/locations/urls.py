from django.urls import path
from locations.views import LastLocationView

urlpatterns = [
    path("api/v1/location/<str:device_id>", LastLocationView.as_view()),
]
