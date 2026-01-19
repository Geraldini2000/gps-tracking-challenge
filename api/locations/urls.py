from django.urls import path
from locations.views import LastLocationView, SimulateHexPacketView

urlpatterns = [
    path("api/v1/location/<str:device_id>", LastLocationView.as_view()),
    path("simulate", SimulateHexPacketView.as_view()),
]
